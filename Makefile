.PHONY: help install backend-install frontend-install backend-dev frontend-dev backend-test frontend-test test docker-build docker-up docker-down clean

help:
	@echo "GitPeek - Makefile Commands"
	@echo "==========================="
	@echo ""
	@echo "Setup:"
	@echo "  make install          - Install all dependencies (backend + frontend)"
	@echo "  make backend-install  - Install backend dependencies"
	@echo "  make frontend-install - Install frontend dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make backend-dev      - Run backend development server"
	@echo "  make frontend-dev     - Run frontend development server"
	@echo "  make dev              - Run both backend and frontend (requires tmux)"
	@echo ""
	@echo "Testing:"
	@echo "  make test             - Run all tests"
	@echo "  make backend-test     - Run backend tests"
	@echo "  make frontend-test    - Run frontend tests"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     - Build Docker images"
	@echo "  make docker-up        - Start Docker containers"
	@echo "  make docker-down      - Stop Docker containers"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            - Clean build artifacts and cache"

install: backend-install frontend-install
	@echo "✓ All dependencies installed"

backend-install:
	@echo "Installing backend dependencies..."
	cd backend && python3 -m venv venv && \
	. venv/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt
	@echo "✓ Backend dependencies installed"

frontend-install:
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✓ Frontend dependencies installed"

backend-dev:
	@echo "Starting backend development server..."
	cd backend && . venv/bin/activate && uvicorn app.main:app --reload

frontend-dev:
	@echo "Starting frontend development server..."
	cd frontend && npm run dev

dev:
	@echo "Starting both backend and frontend..."
	tmux new-session -d -s gitpeek 'cd backend && . venv/bin/activate && uvicorn app.main:app --reload' \; \
	split-window -h 'cd frontend && npm run dev' \; \
	attach-session -t gitpeek

test: backend-test frontend-test
	@echo "✓ All tests completed"

backend-test:
	@echo "Running backend tests..."
	cd backend && . venv/bin/activate && pytest --cov=app --cov-report=term

frontend-test:
	@echo "Running frontend tests..."
	cd frontend && npm test

docker-build:
	@echo "Building Docker images..."
	docker-compose build

docker-up:
	@echo "Starting Docker containers..."
	docker-compose up -d

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf backend/htmlcov backend/.coverage 2>/dev/null || true
	rm -rf frontend/dist frontend/node_modules/.cache 2>/dev/null || true
	rm -rf frontend/coverage 2>/dev/null || true
	@echo "✓ Cleaned"

