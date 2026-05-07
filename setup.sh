#!/bin/bash
# DevDesk Quick Start Script

set -e

echo "🚀 DevDesk Setup Script"
echo "======================"
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

echo "✅ Prerequisites met"
echo ""

# Setup Backend
echo "🔧 Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "  Creating virtual environment..."
    python3 -m venv venv
fi

echo "  Activating virtual environment..."
source venv/bin/activate

echo "  Installing Python dependencies..."
pip install -q -r requirements.txt

echo "✅ Backend setup complete"
echo ""

# Setup Frontend
echo "🔧 Setting up Frontend..."
cd ../frontend

echo "  Installing Node dependencies..."
npm install -q

echo "✅ Frontend setup complete"
echo ""

echo "🎉 Setup Complete!"
echo ""
echo "To run DevDesk:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python src/main.py"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "📱 Dashboard: http://localhost:5173"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
