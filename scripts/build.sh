"""
#!/bin/bash
set -e

# Build script for Flask application

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Load environment variables
source .env 2>/dev/null || true

# Set defaults
ENVIRONMENT=${ENVIRONMENT:-production}
VERSION=${VERSION:-$(git describe --tags --always)}
DOCKER_REGISTRY=${DOCKER_REGISTRY:-local}

echo "Building Flask application..."
echo "Environment: $ENVIRONMENT"
echo "Version: $VERSION"

# Run tests
echo "Running tests..."
cd app
python -m pytest tests/ --cov=app

# Build Docker image
echo "Building Docker image..."
cd "$PROJECT_ROOT"
docker build -t "${DOCKER_REGISTRY}/flask-app:${VERSION}" -f app/Dockerfile app/

# Tag as latest
docker tag "${DOCKER_REGISTRY}/flask-app:${VERSION}" "${DOCKER_REGISTRY}/flask-app:latest"

echo "Build completed successfully!"
"""
