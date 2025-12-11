.PHONY: help install backend-install frontend-install backend-dev frontend-dev backend-test frontend-test test docker-build docker-up docker-down docker-dev clean poetry-install

help:
	@echo "GitPeek - Makefile Commands"
	@echo "==========================="
	@echo ""
	@echo "🐳 Docker Commands (Recommended):"
	@echo "  make docker-up        - Start production containers"
	@echo "  make docker-dev       - Start development containers with hot-reload"
	@echo "  make docker-down      - Stop and remove containers"
	@echo "  make docker-build     - Build Docker images"
	@echo "  make docker-logs      - View container logs"
	@echo "  make docker-clean     - Remove containers, volumes, and images"
	@echo ""
	@echo "📦 Setup (Local Development):"
	@echo "  make install          - Install all dependencies (Poetry + npm)"
	@echo "  make poetry-install   - Install backend with Poetry"
	@echo "  make backend-install  - Install backend dependencies (pip)"
	@echo "  make frontend-install - Install frontend dependencies (npm)"
	@echo ""
	@echo "🚀 Development (Local):"
	@echo "  make backend-dev      - Run backend development server"
	@echo "  make frontend-dev     - Run frontend development server"
	@echo "  make dev              - Run both backend and frontend (requires tmux)"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  make test             - Run all tests"
	@echo "  make backend-test     - Run backend tests"
	@echo "  make frontend-test    - Run frontend tests"
	@echo "  make docker-test      - Run tests in Docker containers"
	@echo ""
	@echo "🧹 Cleanup:"
	@echo "  make clean            - Clean build artifacts and cache"
	@echo "  make docker-clean     - Clean Docker resources"

# =============================================================================
# Docker Commands (Recommended for consistency)
# =============================================================================

docker-up:
	@echo "🚀 Starting GitPeek in production mode..."
	docker-compose up -d
	@echo "✅ GitPeek is running!"
	@echo "   Frontend: http://localhost:3000"
	@echo "   Backend:  http://localhost:8000"
	@echo "   API Docs: http://localhost:8000/docs"

docker-dev:
	@echo "🛠️  Starting GitPeek in development mode..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
	@echo "✅ Development servers started!"
	@echo "   Frontend: http://localhost:5173 (with hot-reload)"
	@echo "   Backend:  http://localhost:8000 (with auto-reload)"

docker-down:
	@echo "🛑 Stopping GitPeek..."
	docker-compose down
	@echo "✅ Stopped"

docker-build:
	@echo "🔨 Building Docker images..."
	docker-compose build --no-cache

docker-logs:
	@echo "📋 Showing logs..."
	docker-compose logs -f

docker-test:
	@echo "🧪 Running tests in Docker..."
	docker-compose exec backend poetry run pytest --cov=app
	docker-compose exec frontend npm test

docker-clean:
	@echo "🧹 Cleaning Docker resources..."
	docker-compose down -v --rmi all --remove-orphans
	@echo "✅ Cleaned"

docker-restart:
	@echo "🔄 Restarting containers..."
	docker-compose restart

docker-ps:
	@echo "📊 Container status:"
	docker-compose ps

# =============================================================================
# Local Development Setup
# =============================================================================

install: poetry-install frontend-install
	@echo "✅ All dependencies installed"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Configure .env files (see .env.example)"
	@echo "  2. Run: make docker-up (Docker) OR make backend-dev & make frontend-dev (Local)"

poetry-install:
	@echo "📦 Installing backend dependencies with Poetry..."
	cd backend && poetry install
	@echo "✅ Backend dependencies installed with Poetry"

backend-install:
	@echo "📦 Installing backend dependencies with pip..."
	cd backend && python3 -m venv venv && \
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt
	@echo "✅ Backend dependencies installed"

frontend-install:
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ Frontend dependencies installed"

# =============================================================================
# Local Development Servers
# =============================================================================

backend-dev:
	@echo "🚀 Starting backend development server..."
	cd backend && poetry run uvicorn app.main:app --reload

frontend-dev:
	@echo "🚀 Starting frontend development server..."
	cd frontend && npm run dev

dev:
	@echo "🚀 Starting both backend and frontend..."
	tmux new-session -d -s gitpeek 'cd backend && poetry run uvicorn app.main:app --reload' \; \
	split-window -h 'cd frontend && npm run dev' \; \
	attach-session -t gitpeek

# =============================================================================
# Testing
# =============================================================================

test: backend-test frontend-test
	@echo "✅ All tests completed"

backend-test:
	@echo "🧪 Running backend tests..."
	cd backend && poetry run pytest --cov=app --cov-report=term

frontend-test:
	@echo "🧪 Running frontend tests..."
	cd frontend && npm test

backend-test-coverage:
	@echo "🧪 Running backend tests with coverage report..."
	cd backend && poetry run pytest --cov=app --cov-report=html
	@echo "📊 Coverage report: backend/htmlcov/index.html"

frontend-test-coverage:
	@echo "🧪 Running frontend tests with coverage report..."
	cd frontend && npm run test:coverage
	@echo "📊 Coverage report: frontend/coverage/index.html"

# =============================================================================
# Code Quality
# =============================================================================

lint:
	@echo "🔍 Running linters..."
	cd backend && poetry run ruff check app/
	cd frontend && npm run lint

format:
	@echo "✨ Formatting code..."
	cd backend && poetry run ruff check --fix app/
	cd frontend && npm run lint -- --fix

# =============================================================================
# Cleanup
# =============================================================================

clean:
	@echo "🧹 Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf backend/htmlcov backend/.coverage 2>/dev/null || true
	rm -rf frontend/dist frontend/node_modules/.cache 2>/dev/null || true
	rm -rf frontend/coverage 2>/dev/null || true
	rm -rf backend/.venv 2>/dev/null || true
	@echo "✅ Cleaned"

clean-all: clean docker-clean
	@echo "✅ Everything cleaned"

# =============================================================================
# Utilities
# =============================================================================

backend-shell:
	@echo "🐚 Opening backend shell..."
	docker-compose exec backend /bin/bash

frontend-shell:
	@echo "🐚 Opening frontend shell..."
	docker-compose exec frontend /bin/sh

db-reset:
	@echo "🗑️  Resetting database..."
	docker-compose down -v
	docker-compose up -d backend
	@echo "✅ Database reset"

env-setup:
	@echo "⚙️  Setting up environment files..."
	@[ ! -f .env ] && cp .env.docker.example .env && echo "Created .env" || echo ".env already exists"
	@[ ! -f backend/.env ] && cp backend/.env.example backend/.env && echo "Created backend/.env" || echo "backend/.env already exists"
	@[ ! -f frontend/.env ] && echo "VITE_API_BASE_URL=http://localhost:8000" > frontend/.env && echo "Created frontend/.env" || echo "frontend/.env already exists"
	@echo "✅ Environment files ready. Please update with your values."

# =============================================================================
# Deployment
# =============================================================================

build-prod:
	@echo "🏗️  Building production images..."
	docker-compose build --no-cache
	@echo "✅ Production images built"

deploy-test:
	@echo "🧪 Testing production build locally..."
	docker-compose up -d
	@echo "Waiting for services to start..."
	sleep 10
	@echo "Testing endpoints..."
	curl -f http://localhost:8000/health || exit 1
	curl -f http://localhost:3000 || exit 1
	@echo "✅ Production build working!"

version:
	@echo "GitPeek Version Info:"
	@echo "  Backend:  $(shell cd backend && poetry version -s)"
	@echo "  Frontend: $(shell cd frontend && node -p "require('./package.json').version")"
	@echo "  Docker:   $(shell docker --version)"
	@echo "  Poetry:   $(shell poetry --version)"
	@echo "  Node:     $(shell node --version)"
