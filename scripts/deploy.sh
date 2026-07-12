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
echo -e "${BLUE}     Freelance Project Finder - Docker Deployment  ${NC}"
echo -e "${BLUE}===================================================${NC}"

# Check docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: docker is not installed or not in PATH.${NC}"
    exit 1
fi

# Check docker compose
if ! docker compose version &> /dev/null; then
    echo -e "${RED}Error: docker compose is not installed or not in PATH.${NC}"
    exit 1
fi

echo -e "${GREEN}✔ Docker and Docker Compose found.${NC}"

# On failure, dump container logs to help with debugging
on_error() {
    echo -e "\n${RED}Deployment failed! Container logs:${NC}"
    docker compose logs || true
}
trap on_error ERR

# Build containers
echo -e "${YELLOW}Building Docker images...${NC}"
docker compose build

# Start containers
echo -e "${YELLOW}Starting containers in detached mode...${NC}"
docker compose up -d

echo -e "${GREEN}✔ Containers launched successfully!${NC}"

# Wait for backend to be ready
echo -e "${YELLOW}Waiting for FastAPI backend to respond...${NC}"
for i in {1..30}; do
    if curl -s -f http://localhost:8010/health &>/dev/null; then
        echo -e "${GREEN}✔ Backend is up and healthy.${NC}"
        break
    fi
    if [ $i -eq 30 ]; then
        echo -e "${RED}Error: Backend failed to start or respond in 30 seconds.${NC}"
        exit 1
    fi
    sleep 1
done

# Seed DB or run collection only if empty
echo -e "${YELLOW}Checking database status...${NC}"
PROJECTS_JSON=$(curl -s http://localhost:8010/projects || echo "[]")
PROJECTS_COUNT=$(python3 -c "import sys, json; data = json.loads(sys.argv[1]); print(len(data)) if isinstance(data, list) else print(0)" "$PROJECTS_JSON" 2>/dev/null || echo "0")

if [ "$PROJECTS_COUNT" = "0" ] || [ -z "$PROJECTS_COUNT" ]; then
    echo -e "${YELLOW}No projects found in database. Seeding sample data...${NC}"
    curl -s -X POST http://localhost:8010/projects/seed > /dev/null
    echo -e "${GREEN}✔ Seeding completed.${NC}"
    
    echo -e "${YELLOW}Starting initial live job collection...${NC}"
    curl -s -X POST http://localhost:8010/collect > /dev/null
    echo -e "${GREEN}✔ Initial collection started/completed.${NC}"
else
    echo -e "${GREEN}✔ Database already contains $PROJECTS_COUNT projects. Skipping initial seed/collect.${NC}"
fi

# Clear error trap since deployment succeeded
trap - ERR

echo -e "${BLUE}===================================================${NC}"
echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${BLUE}You can access the services at:${NC}"
echo -e "  - ${YELLOW}FastAPI API Documentation:${NC} http://localhost:8010/docs"
echo -e "  - ${YELLOW}Streamlit Dashboard:${NC} http://localhost:8501"
echo -e ""
echo -e "Useful Commands:"
echo -e "  - View logs:          ${YELLOW}docker compose logs -f${NC}"
echo -e "  - Stop containers:    ${YELLOW}docker compose down${NC}"
echo -e "  - Restart containers: ${YELLOW}docker compose restart${NC}"
echo -e "${BLUE}===================================================${NC}"
