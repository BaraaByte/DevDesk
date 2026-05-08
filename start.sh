#!/bin/bash

# DevDesk Full Stack Startup Script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
cat << "EOF"
╔══════════════════════════════════════╗
║     DevDesk - v1.0 Development       ║
║    System Monitoring Dashboard       ║
╚══════════════════════════════════════╝
EOF
echo -e "${NC}"

# Get project root
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Shutting down DevDesk...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}✓ DevDesk shut down${NC}"
}

trap cleanup EXIT

echo -e "${YELLOW}Starting DevDesk services...${NC}"
echo ""

# Start backend
echo -e "${BLUE}[Backend]${NC} Starting on http://127.0.0.1:8000"
cd "$PROJECT_ROOT/backend"
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}[Backend]${NC} Creating virtual environment..."
    python3 -m venv .venv
fi
source .venv/bin/activate
if ! python -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}[Backend]${NC} Installing dependencies..."
    pip install -q -r requirements.txt
fi
python app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

# Start frontend
echo -e "${BLUE}[Frontend]${NC} Starting on http://localhost:5173"
cd "$PROJECT_ROOT/frontend"
if ! command -v npm &> /dev/null; then
    echo -e "${RED}[Frontend]${NC} npm not found. Please install Node.js"
    exit 1
fi
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}[Frontend]${NC} Installing dependencies..."
    npm install --quiet 2>/dev/null
fi
npm run dev &
FRONTEND_PID=$!

echo ""
echo -e "${GREEN}✓ DevDesk is running!${NC}"
echo ""
echo -e "${BLUE}Services:${NC}"
echo "  • Frontend: http://localhost:5173"
echo "  • Backend:  http://127.0.0.1:8000"
echo "  • API Docs: http://127.0.0.1:8000"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
