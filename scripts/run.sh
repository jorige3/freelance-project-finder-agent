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
echo -e "${BLUE}        Freelance Project Finder - Startup          ${NC}"
echo -e "${BLUE}===================================================${NC}"

# Check virtual environment
if [ ! -d ".venv" ]; then
    echo -e "${RED}Error: .venv directory not found. Please run setup first:${NC}"
    echo -e "  ./scripts/setup.sh"
    exit 1
fi

# Set local mode environment variables
export API_BASE_URL="http://localhost:8010"
export DATABASE_URL="sqlite:///./freelance_projects.db"

# Check if backend is already running
BACKEND_ALREADY_RUNNING=false
BACKEND_PID=""

if curl -s -f http://localhost:8010/health &>/dev/null; then
    echo -e "${YELLOW}Warning: Backend is already running on port 8010. Reusing existing backend.${NC}"
    BACKEND_ALREADY_RUNNING=true
elif lsof -Pi :8010 -sTCP:LISTEN -t &>/dev/null || ss -tuln | grep -q ":8010 "; then
    echo -e "${RED}Error: Port 8010 is occupied by another process, but the backend health check failed.${NC}"
    exit 1
fi

# Cleanup function to kill child processes on exit/Ctrl+C
cleanup() {
    # Disable exit on error for cleanup commands
    set +e
    echo -e "\n${YELLOW}Stopping local services...${NC}"
    if [ "$BACKEND_ALREADY_RUNNING" = false ] && [ -n "${BACKEND_PID}" ]; then
        echo -e "Stopping FastAPI backend (PID: $BACKEND_PID)..."
        kill "$BACKEND_PID" 2>/dev/null || true
    fi
    echo -e "${GREEN}✔ Cleanup finished.${NC}"
}
trap cleanup INT TERM EXIT

# Start FastAPI backend if not already running
if [ "$BACKEND_ALREADY_RUNNING" = false ]; then
    echo -e "${YELLOW}Starting FastAPI Backend on port 8010...${NC}"
    # Use uv run to run uvicorn
    uv run uvicorn app.main:app --host 0.0.0.0 --port 8010 > backend.log 2>&1 &
    BACKEND_PID=$!
    echo -e "${GREEN}✔ Backend started in background with PID: $BACKEND_PID (logs in backend.log)${NC}"
    
    # Wait for backend to be ready
    echo -e "${YELLOW}Waiting for FastAPI server to respond...${NC}"
    for i in {1..30}; do
        if curl -s -f http://localhost:8010/health &>/dev/null; then
            echo -e "${GREEN}✔ Backend is healthy and responding!${NC}"
            break
        fi
        if [ $i -eq 30 ]; then
            echo -e "${RED}Error: Backend failed to start in 30 seconds. Check backend.log for details.${NC}"
            exit 1
        fi
        sleep 1
    done
fi

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

# Start Streamlit Frontend
echo -e "${BLUE}===================================================${NC}"
echo -e "${GREEN}Starting Streamlit Dashboard on port 8501...${NC}"
echo -e "${BLUE}You can access the services at:${NC}"
echo -e "  - ${YELLOW}FastAPI API Documentation:${NC} http://localhost:8010/docs"
echo -e "  - ${YELLOW}Streamlit Dashboard:${NC} http://localhost:8501"
echo -e "${BLUE}===================================================${NC}"

# Run Streamlit in the foreground
uv run streamlit run dashboard/app.py --server.port 8501 --server.address 0.0.0.0
