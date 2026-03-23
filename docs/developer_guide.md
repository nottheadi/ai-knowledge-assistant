# Developer Guide

This guide helps new contributors get started with development.

## Setup
- Clone the repo: `git clone https://github.com/nottheadi/ai-knowledge-assistant.git`
- Install dependencies: `pip install -r apps/backend/requirements.txt`
- (Optional) Install dev dependencies: `pip install -r apps/backend/requirements-dev.txt`
- Set up `.env` file in `apps/backend/` with required variables (see `.env.example`):
	- `GEMINI_API_KEY`
	- `MODEL`
- Run the app: `cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

## Testing
- Run tests: `pytest apps/backend/tests`
- Lint: `flake8 apps/backend/app`
- Format: `black apps/backend/app && isort apps/backend/app`

## Contributing
- Follow code style and add docstrings (see CONTRIBUTING.md)
- Write tests for new features and bug fixes
- Open a pull request for review

See CONTRIBUTING.md for more details.
