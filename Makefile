.PHONY: help install test lint format docker-up docker-down clean

help:
	@echo "RAGLedger Makefile"
	@echo "Available commands:"
	@echo "  make install      - Install all dependencies"
	@echo "  make test         - Run all tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make clean        - Clean build artifacts"

install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

test:
	@echo "Running backend tests..."
	cd backend && pytest tests/ -v
	@echo "Running frontend tests..."
	cd frontend && npm test

lint:
	@echo "Linting backend..."
	cd backend && flake8 . --max-line-length=100
	@echo "Linting frontend..."
	cd frontend && npm run lint

format:
	@echo "Formatting backend..."
	cd backend && black . --line-length=100
	@echo "Formatting frontend..."
	cd frontend && npm run format

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	@echo "Cleaning build artifacts..."
	rm -rf backend/__pycache__ backend/**/__pycache__ backend/.pytest_cache
	rm -rf frontend/node_modules frontend/dist frontend/.vite
	rm -rf .terraform terraform.tfstate* .terraform.lock.hcl

