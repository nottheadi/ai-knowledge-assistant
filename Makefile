
# Makefile for AI Knowledge Assistant
# Maintainer: Senior Software Developer
# Improvements: variables, portability, error handling, stop/check targets

.PHONY: help backend-setup backend-run backend-test backend-lint backend-format backend-clean backend-all frontend-setup frontend-run frontend-build frontend-test frontend-lint frontend-format frontend-clean frontend-all all clean stop check-deps

# Variables
PYTHON ?= python3
PIP ?= pip3
BACKEND_DIR := backend
FRONTEND_DIR := frontend
FRONTEND_NODE_MODULES := $(FRONTEND_DIR)/node_modules
FRONTEND_DIST := $(FRONTEND_DIR)/dist
BACKEND_PY_CACHE := $(BACKEND_DIR)/.pytest_cache


help:
	@echo "Available targets:"
	@echo "  all                 Setup and build both backend and frontend"
	@echo "  setup               Setup both backend and frontend dependencies"
	@echo "  run                 Run both backend and frontend apps (dev mode)"
	@echo "  stop                Stop all background backend/frontend processes"
	@echo "  check-deps          Check required tools (python, pip, npm, etc)"
	@echo "  backend-setup       Install backend dependencies (prod + dev)"
	@echo "  backend-run         Run the FastAPI backend app (dev mode)"
	@echo "  backend-test        Run all backend tests with pytest"
	@echo "  backend-lint        Run backend linting (flake8)"
	@echo "  backend-format      Format backend code (black, isort)"
	@echo "  backend-clean       Clean backend build artifacts"
	@echo "  backend-all         Setup, lint, format, test backend"
	@echo "  frontend-setup      Install frontend dependencies (npm install)"
	@echo "  frontend-run        Run Angular dev server (ng serve)"
	@echo "  frontend-build      Build Angular app (ng build)"
	@echo "  frontend-test       Run Angular unit tests (ng test)"
	@echo "  frontend-lint       Lint Angular code (eslint)"
	@echo "  frontend-format     Format Angular code (prettier)"
	@echo "  frontend-clean      Clean frontend build artifacts"
	@echo "  frontend-all        Setup, lint, format, test, build frontend"
	@echo "  clean               Clean all build artifacts (backend + frontend)"

# Check for required tools
check-deps:
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo >&2 "$(PYTHON) not found. Please install Python."; exit 1; }
	@command -v $(PIP) >/dev/null 2>&1 || { echo >&2 "$(PIP) not found. Please install pip."; exit 1; }
	@command -v npm >/dev/null 2>&1 || { echo >&2 "npm not found. Please install Node.js and npm."; exit 1; }
	@command -v npx >/dev/null 2>&1 || { echo >&2 "npx not found. Please install Node.js and npm."; exit 1; }

# Generic setup for both backend and frontend
setup: check-deps
	$(MAKE) backend-setup
	$(MAKE) frontend-setup
# Format both backend and frontend code
format:
	$(MAKE) backend-format
	$(MAKE) frontend-format
# Generic run for both backend and frontend (in separate terminals)
run: check-deps
	@echo "Starting backend (background)..."
	( cd $(BACKEND_DIR) && $(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 ) & echo $$! > backend.pid
	@echo "Backend running with PID $$(cat backend.pid)."
	@echo "Starting frontend (background)..."
	( cd $(FRONTEND_DIR) && npm run start ) & echo $$! > frontend.pid
	@echo "Frontend running with PID $$(cat frontend.pid)."
	@echo "Both backend and frontend are running in the background. Use 'make stop' to stop them."

# Stop background backend/frontend processes
stop:
	-@if [ -f backend.pid ]; then kill $$(cat backend.pid) 2>/dev/null || true; rm backend.pid; echo "Stopped backend."; fi
	-@if [ -f frontend.pid ]; then kill $$(cat frontend.pid) 2>/dev/null || true; rm frontend.pid; echo "Stopped frontend."; fi


backend-setup:
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r $(BACKEND_DIR)/requirements.txt
	$(PIP) install --upgrade -r $(BACKEND_DIR)/requirements-dev.txt


backend-run:
	cd $(BACKEND_DIR) && $(PYTHON) -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


backend-test:
	cd $(BACKEND_DIR) && pytest tests


backend-lint:
	flake8 $(BACKEND_DIR)/app


backend-format:
	black $(BACKEND_DIR)/app
	isort $(BACKEND_DIR)/app


backend-clean:
	find $(BACKEND_DIR) -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf $(BACKEND_PY_CACHE)


# --- Grouped targets ---


all: backend-all frontend-all

backend-all: backend-setup backend-lint backend-format backend-test

frontend-all: frontend-setup frontend-lint frontend-format frontend-test frontend-build


frontend-setup:
	cd $(FRONTEND_DIR) && npm install


frontend-run:
	cd $(FRONTEND_DIR) && npm run start


frontend-build:
	cd $(FRONTEND_DIR) && npm run build


frontend-test:
	cd $(FRONTEND_DIR) && npm run test -- --watch=false


frontend-lint:
	cd $(FRONTEND_DIR) && npx eslint ./src --ext .ts,.js,.html


frontend-format:
	cd $(FRONTEND_DIR) && npx prettier --write "src/**/*.{ts,js,html,css,scss}"


frontend-clean:
	rm -rf $(FRONTEND_DIST) $(FRONTEND_NODE_MODULES)

# Clean all build artifacts (backend + frontend)
clean:
	$(MAKE) backend-clean
	$(MAKE) frontend-clean
