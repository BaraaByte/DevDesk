#!/bin/bash

# DevDesk Backend Startup Script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to backend directory
cd "$SCRIPT_DIR"

echo -e "${YELLOW}DevDesk Backend${NC}"
echo "================"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv .venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source .venv/bin/activate

# Check if dependencies are installed
if ! python -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

# Check if database needs to be recreated
if [ -z "$1" ] || [ "$1" != "--reset-db" ]; then
    # Start the server
    echo -e "${GREEN}✓ Starting DevDesk Backend on http://127.0.0.1:8000${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
    echo ""
    python app.py
else
    # Reset database
    echo -e "${YELLOW}Resetting database...${NC}"
    rm -f devdesk_dev.db devdesk.db
    echo -e "${GREEN}✓ Database reset${NC}"
    echo -e "${GREEN}✓ Starting DevDesk Backend on http://127.0.0.1:8000${NC}"
    python app.py
fi
