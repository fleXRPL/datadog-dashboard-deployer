#!/bin/bash

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting build and publish process...${NC}\n"

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
    rm -rf .venv/ build/ dist/ *.egg-info/
    echo -e "${GREEN}✓ Cleanup completed${NC}\n"
}

# Set up trap to clean up on script exit
trap cleanup EXIT

# Create and activate virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv .venv
source .venv/bin/activate
echo -e "${GREEN}✓ Virtual environment created and activated${NC}\n"

# Install build dependencies
echo -e "${YELLOW}Installing build dependencies...${NC}"
python -m pip install --upgrade pip
pip install build twine
echo -e "${GREEN}✓ Build dependencies installed${NC}\n"

# Clean previous builds
echo -e "${YELLOW}Cleaning previous builds...${NC}"
rm -rf build/ dist/ *.egg-info/
echo -e "${GREEN}✓ Previous builds cleaned${NC}\n"

# Build package
run_check "Building package" "python -m build"

# Check distribution
run_check "Checking distribution" "twine check dist/*"

# Upload to PyPI if PYPI_TOKEN is set
if [ -n "$PYPI_TOKEN" ]; then
    echo -e "${YELLOW}Uploading to PyPI...${NC}"
    TWINE_USERNAME=__token__ TWINE_PASSWORD=$PYPI_TOKEN twine upload dist/*
    echo -e "${GREEN}✓ Package uploaded to PyPI${NC}\n"
else
    echo -e "${YELLOW}PYPI_TOKEN not set, skipping upload${NC}\n"
fi

echo -e "${GREEN}Build and publish process completed successfully!${NC}" 