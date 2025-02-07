#!/bin/bash

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo -e "${YELLOW}Starting local environment setup...${NC}\n"

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

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}Found Python $PYTHON_VERSION${NC}\n"
else
    echo -e "${RED}Python 3 not found. Please install Python 3.8 or higher${NC}\n"
    exit 1
fi

# Create and activate virtual environment
echo -e "${YELLOW}Setting up virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Found existing virtual environment. Removing...${NC}"
    rm -rf venv
fi

run_check "Creating virtual environment" "python3 -m venv venv"
source venv/bin/activate

# Upgrade pip and install dependencies
run_check "Upgrading pip" "python -m pip install --upgrade pip"
run_check "Installing development dependencies" "pip install -r requirements-dev.txt"
run_check "Installing package in editable mode" "pip install -e ."

# Set up pre-commit hooks
run_check "Setting up pre-commit hooks" "pre-commit install"

# Create config directory if it doesn't exist
if [ ! -d "config" ]; then
    echo -e "${YELLOW}Creating config directory...${NC}"
    mkdir -p config
fi

# Check for DataDog credentials
echo -e "${YELLOW}Checking DataDog credentials...${NC}"
if [ -z "${DATADOG_API_KEY}" ] || [ -z "${DATADOG_APP_KEY}" ]; then
    echo -e "${YELLOW}DataDog credentials not found in environment.${NC}"
    echo -e "${YELLOW}Please set up your credentials by running:${NC}"
    echo -e "export DATADOG_API_KEY='your-api-key'"
    echo -e "export DATADOG_APP_KEY='your-application-key'"
    echo -e "\n${YELLOW}You can add these to your ~/.bashrc or ~/.zshrc for persistence${NC}"
fi

# Create example configuration if it doesn't exist
if [ ! -f "config/dashboard_config.yaml" ]; then
    echo -e "${YELLOW}Creating example dashboard configuration...${NC}"
    cat > config/dashboard_config.yaml << EOL
version: "1.0"
dashboards:
  - name: "Example Dashboard"
    description: "Example dashboard configuration"
    widgets:
      - title: "CPU Usage"
        type: "timeseries"
        query: "avg:system.cpu.user{*}"
      - title: "Memory Usage"
        type: "timeseries"
        query: "avg:system.mem.used{*}"
EOL
    echo -e "${GREEN}✓ Created example configuration${NC}\n"
fi

echo -e "${GREEN}Local environment setup complete!${NC}\n"
echo -e "Next steps:"
echo -e "1. Set up your DataDog credentials if you haven't already"
echo -e "2. Review and modify config/dashboard_config.yaml"
echo -e "3. Run 'datadog-dashboard-deploy config/dashboard_config.yaml' to deploy your first dashboard"
echo -e "\nFor more information, visit: https://github.com/fleXRPL/datadog-dashboard-deployer/wiki/Getting-Started" 