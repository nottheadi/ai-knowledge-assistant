# FAQ / Troubleshooting

## How do I get started quickly?
- See the Quickstart section in the main README.md for setup and first run instructions.
- Install dependencies with `pip install -r backend/requirements.txt`.
- Set up your `.env` file in `backend/` (see `.env.example`).
- Run the app with `cd backend && uvicorn app.main:app --reload`.

## Why does my PDF upload fail?
- Only PDF files are accepted (must have `.pdf` extension).
- File size must be under 10MB.
- The file must have a valid PDF signature (first 4 bytes are `%PDF`).
- Check that your request uses the correct form data key: `file`.

## How do I use RAG chat?
- Use the `/api/chat/RAG` endpoint with a JSON body: `{ "query": "your question" }`.
- Make sure you have uploaded at least one PDF document first.

## Where can I find API details?
- See `backend/docs/api.md` or the live Swagger UI at `/docs` when the app is running.

## How do I contribute?
- See CONTRIBUTING.md and the Developer Guide in `backend/docs/`.

## How do I report a bug or request a feature?
- Open an issue on GitHub with details and steps to reproduce.

Add more Q&A as the project grows.