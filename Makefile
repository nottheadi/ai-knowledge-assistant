# Makefile for AI Knowledge Assistant

.PHONY: help setup run test lint format clean

help:
	@echo "Available targets:"
	@echo "  setup   Install all dependencies (prod + dev)"
	@echo "  run     Run the FastAPI app (dev mode)"
	@echo "  test    Run all tests with pytest"
	@echo "  lint    Run flake8 for linting"
	@echo "  format  Run black and isort for formatting"
	@echo "  clean   Remove __pycache__ and .pytest_cache__"

setup:
	pip install -r backend/requirement.txt
	pip install -r backend/requirements-dev.txt

run:
	cd backend && /home/codespace/.python/current/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest backend/tests

lint:
	flake8 backend/app

format:
	black backend/app
	isort backend/app

clean:
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf backend/.pytest_cache
