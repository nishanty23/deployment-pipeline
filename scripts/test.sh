"""
#!/bin/bash
set -e

# Test script for Flask application
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=== Flask Application Test Suite ==="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
print_status "Installing dependencies..."
cd app
pip install -r requirements.txt
pip install pytest-cov pytest-mock pytest-flask

# Create test directory if it doesn't exist
if [ ! -d "tests" ]; then
    print_status "Creating tests directory..."
    mkdir tests
    touch tests/__init__.py
    
    # Create sample test file
    cat > tests/test_app.py << 'EOF'
import pytest
import json
from app import create_app

@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

def test_health_check(client):
    """Test health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert 'version' in data

def test_home_endpoint(client):
    """Test home endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'environment' in data
    assert 'version' in data

def test_api_data_endpoint(client):
    """Test API data endpoint."""
    response = client.get('/api/data')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'data' in data
    assert 'timestamp' in data
    assert isinstance(data['data'], list)

def test_invalid_endpoint(client):
    """Test invalid endpoint returns 404."""
    response = client.get('/invalid-endpoint')
    assert response.status_code == 404
EOF
fi

# Run linting if flake8 is available
if command -v flake8 &> /dev/null; then
    print_status "Running code linting..."
    flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || print_warning "Linting found issues"
    flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics || print_warning "Style issues found"
else
    print_warning "flake8 not found, skipping linting"
fi

# Run security checks if bandit is available
if command -v bandit &> /dev/null; then
    print_status "Running security checks..."
    bandit -r . -f json -o bandit-report.json || print_warning "Security issues found"
else
    print_warning "bandit not found, skipping security checks"
fi

# Run tests with coverage
print_status "Running unit tests with coverage..."
python -m pytest tests/ \
    --verbose \
    --cov=. \
    --cov-report=term-missing \
    --cov-report=html:htmlcov \
    --cov-report=xml:coverage.xml \
    --cov-fail-under=80 \
    --tb=short

# Run integration tests if they exist
if [ -d "tests/integration" ]; then
    print_status "Running integration tests..."
    python -m pytest tests/integration/ --verbose
fi

# Check if coverage meets minimum threshold
COVERAGE_THRESHOLD=80
if [ -f "coverage.xml" ]; then
    COVERAGE=$(python -c "
import xml.etree.ElementTree as ET
tree = ET.parse('coverage.xml')
root = tree.getroot()
coverage = float(root.attrib['line-rate']) * 100
print(f'{coverage:.1f}')
")
    
    print_status "Test coverage: ${COVERAGE}%"
    
    if (( $(echo "$COVERAGE < $COVERAGE_THRESHOLD" | bc -l) )); then
        print_error "Coverage ${COVERAGE}% is below threshold ${COVERAGE_THRESHOLD}%"
        exit 1
    else
        print_status "Coverage requirement met"
    fi
fi

# Generate test report
print_status "Generating test report..."
cat > test-report.txt << EOF
=== Test Report ===
Date: $(date)
Environment: ${FLASK_ENV:-testing}
Coverage: ${COVERAGE:-N/A}%
Tests: $(grep -c "def test_" tests/*.py 2>/dev/null || echo "0")

Test files:
$(find tests -name "*.py" -exec basename {} \; | sort)

EOF

# Performance test if available
if [ -f "tests/performance_test.py" ]; then
    print_status "Running performance tests..."
    python tests/performance_test.py
fi

# Clean up temporary files
print_status "Cleaning up..."
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

print_status "All tests completed successfully!"

# Display summary
echo ""
echo "=== Test Summary ==="
echo "Unit tests: PASSED"
echo "Coverage: ${COVERAGE:-N/A}% (threshold: ${COVERAGE_THRESHOLD}%)"
echo "Report generated: test-report.txt"
echo "Coverage report: htmlcov/index.html"
echo ""
"""
