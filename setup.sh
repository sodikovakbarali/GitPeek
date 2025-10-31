#!/bin/bash

# GitPeek Setup Script
# This script helps you set up the development environment

set -e

echo "🚀 GitPeek Setup Script"
echo "======================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📦 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Check Node version
echo "📦 Checking Node.js version..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

NODE_VERSION=$(node --version)
echo -e "${GREEN}✓ Node.js $NODE_VERSION found${NC}"
echo ""

# Backend setup
echo "🔧 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing backend dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating backend .env file..."
    cat > .env << EOL
GITHUB_CLIENT_ID=your_github_client_id_here
GITHUB_CLIENT_SECRET=your_github_client_secret_here
GITHUB_REDIRECT_URI=http://localhost:5173/auth/callback
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
DATABASE_URL=sqlite+aiosqlite:///./gitpeek.db
CACHE_EXPIRE_MINUTES=10
GITHUB_API_BASE_URL=https://api.github.com
GITHUB_GRAPHQL_URL=https://api.github.com/graphql
EOL
    echo -e "${YELLOW}⚠️  Please update GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET in backend/.env${NC}"
fi

echo -e "${GREEN}✓ Backend setup complete${NC}"
cd ..

# Frontend setup
echo ""
echo "🔧 Setting up frontend..."
cd frontend

# Install dependencies
echo "Installing frontend dependencies..."
npm install > /dev/null 2>&1

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating frontend .env file..."
    echo "VITE_API_BASE_URL=http://localhost:8000" > .env
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"
cd ..

# Summary
echo ""
echo "✨ Setup Complete!"
echo "=================="
echo ""
echo -e "${GREEN}Backend:${NC}"
echo "  1. Update backend/.env with your GitHub OAuth credentials"
echo "  2. cd backend && source venv/bin/activate"
echo "  3. uvicorn app.main:app --reload"
echo ""
echo -e "${GREEN}Frontend:${NC}"
echo "  1. cd frontend"
echo "  2. npm run dev"
echo ""
echo -e "${YELLOW}📝 Note: To enable GitHub OAuth login, create an OAuth app at:${NC}"
echo -e "${YELLOW}   https://github.com/settings/developers${NC}"
echo ""
echo "🎉 Happy coding!"

