"""
#!/bin/bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

ENVIRONMENT=${1:-production}

echo "Initiating rollback for $ENVIRONMENT environment..."

python deployment/deploy.py --environment "$ENVIRONMENT" --action rollback

echo "Rollback completed!"
"""
