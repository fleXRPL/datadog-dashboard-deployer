#!/bin/bash

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting test and lint checks...${NC}\n"

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Function to run a command and check its status
run_check() {
    echo -e "${YELLOW}Running $1...${NC}"
    if eval "$2"; then
        echo -e "${GREEN}✓ $1 passed${NC}\n"
    else
        echo -e "${RED}✗ $1 failed${NC}\n"
        exit 1
    fi
}

# Function to clean up
cleanup() {
    echo -e "\n${YELLOW}Cleaning up...${NC}"
    deactivate 2>/dev/null || true
    rm -rf .venv/
    echo -e "${GREEN}✓ Cleanup completed${NC}\n"
}

# Set up trap to clean up on script exit
trap cleanup EXIT

# Create and activate virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv .venv
source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment created and activated${NC}\n"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pip install -e .
echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Format code
echo -e "${YELLOW}Current directory: $(pwd)${NC}"
echo -e "${YELLOW}Project root: ${PROJECT_ROOT}${NC}"
echo -e "${YELLOW}Running black on: ${PROJECT_ROOT}/src/datadog_dashboard_deployer ${PROJECT_ROOT}/tests${NC}"

# Run black and isort to actually format the files (without --check)
run_check "Black formatting" "black src/datadog_dashboard_deployer tests"
run_check "isort" "isort src/datadog_dashboard_deployer tests"

# Then run flake8 which is check-only
run_check "Flake8 linting" "flake8 src/datadog_dashboard_deployer tests"

# Run tests with coverage
run_check "Pytest with coverage" "pytest tests/ --cov=datadog_dashboard_deployer --cov-report=term-missing --cov-fail-under=90"

# Generate coverage report
echo -e "${YELLOW}Generating HTML coverage report...${NC}"
coverage html
echo -e "${GREEN}Coverage report generated in htmlcov/index.html${NC}\n"

echo -e "${GREEN}All checks passed successfully!${NC}" 