# Developer Guide

This guide helps new contributors get started with development.

## Setup
- Clone the repo
- Install dependencies: `pip install -r backend/requirement.txt`
- Set up `.env` file with required variables
- Run the app: `uvicorn app.main:app --reload`

## Testing
- Run tests: `pytest backend/tests`
- Lint: `flake8 backend/app`
- Format: `black backend/app`

## Contributing
- Follow code style and add docstrings
- Write tests for new features
- Open a pull request for review

See CONTRIBUTING.md for more details.
