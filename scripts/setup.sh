#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status,
# if an uninitialized variable is used, or if any command in a pipeline fails.
set -euo pipefail

# Define colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}===================================================${NC}"
echo -e "${BLUE}   Freelance Project Finder - Setup & Compilation   ${NC}"
echo -e "${BLUE}===================================================${NC}"

# Check for uv
if ! command -v uv &> /dev/null; then
    echo -e "${RED}Error: uv dependency manager is not installed.${NC}"
    echo -e "Please install uv before proceeding:"
    echo -e "  ${YELLOW}curl -LsSf https://astral.sh/uv/install.sh | sh${NC}"
    exit 1
fi
echo -e "${GREEN}✔ Found uv: $(uv --version)${NC}"

# Check python3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed. Please install it first.${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "${GREEN}✔ Found Python: $PYTHON_VERSION${NC}"

# Sync dependencies using uv (creates .venv if missing and installs dependencies locked)
echo -e "${YELLOW}Syncing dependencies using uv sync...${NC}"
uv sync

echo -e "${GREEN}✔ All dependencies synchronized successfully.${NC}"

# Check database status
echo -e "${YELLOW}Checking database status...${NC}"
if [ ! -f "freelance_projects.db" ]; then
    echo -e "${YELLOW}Database file not found. It will be automatically created and seeded on first run.${NC}"
else
    echo -e "${GREEN}✔ Database 'freelance_projects.db' exists.${NC}"
fi

echo -e "${BLUE}===================================================${NC}"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "You can run the project using: ${YELLOW}./scripts/run.sh${NC}"
echo -e "${BLUE}===================================================${NC}"
