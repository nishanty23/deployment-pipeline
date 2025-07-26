import os
import sys
import subprocess
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional

class DeploymentPipeline:
    def __init__(self, environment: str = 'production'):
        self.environment = environment
        self.project_root = Path(__file__).parent.parent
        self.app_name = 'flask-app'
        self.version = self._get_version()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Load environment config
        self.config = self._load_config()
        
    def _get_version(self) -> str:
        """Get version from git tag or commit hash"""
        try:
            result = subprocess.run(
                ['git', 'describe', '--tags', '--always'],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            return result.stdout.strip() or 'latest'
        except:
            return 'latest'
    
    def _load_config(self) -> Dict:
        """Load environment-specific configuration"""
        config_file = self.project_root / 'config' / f'{self.environment}.py'
        if config_file.exists():
            # In a real scenario, you'd properly import the config
            return {
                'docker_registry': 'your-registry.com',
                'namespace': 'flask-app',
                'replicas': 3 if self.environment == 'production' else 1,
                'domain': f'{self.environment}.yourdomain.com'
            }
        return {}
    
    def run_tests(self) -> bool:
        """Run test suite"""
        self.logger.info("Running tests...")
        try:
            result = subprocess.run([
                'python', '-m', 'pytest',
                'tests/',
                '--cov=app',
                '--cov-report=xml'
            ], cwd=self.project_root, check=True)
            self.logger.info("Tests passed successfully")
            return True
        except subprocess.CalledProcessError:
            self.logger.error("Tests failed")
            return False
    
    def build_docker_image(self) -> bool:
        """Build Docker image"""
        image_tag = f"{self.config.get('docker_registry', 'local')}/{self.app_name}:{self.version}"
        self.logger.info(f"Building Docker image: {image_tag}")
        
        try:
            subprocess.run([
                'docker', 'build',
                '-t', image_tag,
                '-f', 'app/Dockerfile',
                'app/'
            ], cwd=self.project_root, check=True)
            
            self.logger.info("Docker image built successfully")
            return True
        except subprocess.CalledProcessError:
            self.logger.error("Docker build failed")
            return False
    
    def push_docker_image(self) -> bool:
        """Push Docker image to registry"""
        if self.config.get('docker_registry') == 'local':
            self.logger.info("Skipping push for local registry")
            return True
            
        image_tag = f"{self.config['docker_registry']}/{self.app_name}:{self.version}"
        self.logger.info(f"Pushing Docker image: {image_tag}")
        
        try:
            subprocess.run(['docker', 'push', image_tag], check=True)
            self.logger.info("Docker image pushed successfully")
            return True
        except subprocess.CalledProcessError:
            self.logger.error("Docker push failed")
            return False
    
    def deploy_with_docker_compose(self) -> bool:
        """Deploy using Docker Compose"""
        self.logger.info("Deploying with Docker Compose...")
        
        # Set environment variables
        env = os.environ.copy()
        env.update({
            'APP_VERSION': self.version,
            'FLASK_ENV': self.environment,
            'COMPOSE_PROJECT_NAME': f"{self.app_name}-{self.environment}"
        })
        
        try:
            # Pull latest images
            subprocess.run([
                'docker-compose', '-f', 'deployment/docker-compose.yml',
                'pull'
            ], cwd=self.project_root, env=env, check=True)
            
            # Deploy with zero-downtime
            subprocess.run([
                'docker-compose', '-f', 'deployment/docker-compose.yml',
                'up', '-d', '--remove-orphans'
            ], cwd=self.project_root, env=env, check=True)
            
            self.logger.info("Deployment completed successfully")
            return True
        except subprocess.CalledProcessError:
            self.logger.error("Deployment failed")
            return False
    
    def health_check(self, max_retries: int = 30) -> bool:
        """Perform health check on deployed application"""
        self.logger.info("Performing health check...")
        
        import requests
        health_url = f"http://localhost:5000/health"
        
        for i in range(max_retries):
            try:
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    self.logger.info("Health check passed")
                    return True
            except requests.RequestException:
                pass
            
            self.logger.info(f"Health check attempt {i+1}/{max_retries} failed, retrying...")
            time.sleep(10)
        
        self.logger.error("Health check failed")
        return False
    
    def rollback(self) -> bool:
        """Rollback to previous version"""
        self.logger.info("Initiating rollback...")
        
        try:
            # Get previous version from deployment history
            result = subprocess.run([
                'docker', 'images', '--format', 'table {{.Tag}}',
                f"{self.config.get('docker_registry', 'local')}/{self.app_name}"
            ], capture_output=True, text=True)
            
            versions = [line.strip() for line in result.stdout.split('\n')[1:] if line.strip()]
            if len(versions) < 2:
                self.logger.error("No previous version found for rollback")
                return False
            
            previous_version = versions[1]  # Second most recent
            self.logger.info(f"Rolling back to version: {previous_version}")
            
            # Update environment variable and redeploy
            env = os.environ.copy()
            env.update({
                'APP_VERSION': previous_version,
                'FLASK_ENV': self.environment
            })
            
            subprocess.run([
                'docker-compose', '-f', 'deployment/docker-compose.yml',
                'up', '-d'
            ], cwd=self.project_root, env=env, check=True)
            
            self.logger.info("Rollback completed successfully")
            return True
        except subprocess.CalledProcessError:
            self.logger.error("Rollback failed")
            return False
    
    def cleanup_old_images(self, keep_count: int = 5) -> None:
        """Clean up old Docker images"""
        self.logger.info("Cleaning up old Docker images...")
        
        try:
            # Remove unused images
            subprocess.run(['docker', 'image', 'prune', '-f'], check=True)
            
            # Remove old versions (keep only specified count)
            result = subprocess.run([
                'docker', 'images', '--format', '{{.ID}} {{.Tag}}',
                f"{self.config.get('docker_registry', 'local')}/{self.app_name}"
            ], capture_output=True, text=True)
            
            lines = result.stdout.strip().split('\n')
            if len(lines) > keep_count:
                old_images = lines[keep_count:]
                for line in old_images:
                    image_id = line.split()[0]
                    subprocess.run(['docker', 'rmi', image_id], check=True)
            
            self.logger.info("Cleanup completed")
        except subprocess.CalledProcessError:
            self.logger.warning("Cleanup encountered some issues")
    
    def deploy(self) -> bool:
        """Execute full deployment pipeline"""
        self.logger.info(f"Starting deployment pipeline for {self.environment} environment")
        
        steps = [
            ("Running tests", self.run_tests),
            ("Building Docker image", self.build_docker_image),
            ("Pushing Docker image", self.push_docker_image),
            ("Deploying application", self.deploy_with_docker_compose),
            ("Health check", self.health_check)
        ]
        
        for step_name, step_func in steps:
            self.logger.info(f"Step: {step_name}")
            if not step_func():
                self.logger.error(f"Pipeline failed at step: {step_name}")
                self.logger.info("Initiating rollback...")
                self.rollback()
                return False
        
        # Cleanup old images after successful deployment
        self.cleanup_old_images()
        
        self.logger.info("Deployment pipeline completed successfully!")
        return True

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Flask Application Deployment Pipeline')
    parser.add_argument('--environment', '-e', default='production',
                       choices=['development', 'staging', 'production'],
                       help='Deployment environment')
    parser.add_argument('--action', '-a', default='deploy',
                       choices=['deploy', 'rollback', 'health-check'],
                       help='Action to perform')
    
    args = parser.parse_args()
    
    pipeline = DeploymentPipeline(args.environment)
    
    if args.action == 'deploy':
        success = pipeline.deploy()
    elif args.action == 'rollback':
        success = pipeline.rollback()
    elif args.action == 'health-check':
        success = pipeline.health_check()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
