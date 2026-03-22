# Frontend

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 21.2.3.

## Development server

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

## Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

## Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

## Running unit tests

To execute unit tests with the [Vitest](https://vitest.dev/) test runner, use the following command:

```bash
ng test
```

## Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.


## API Integration

This frontend communicates with the AI Knowledge Assistant backend via HTTP API endpoints. The main API interactions are:

- **Upload PDF:**
	- `POST /api/upload` — Upload a PDF file for processing.
- **List Uploaded PDFs:**
	- `GET /api/uploads` — Retrieve a list of all uploaded PDF filenames.
- **Chat with AI:**
	- `POST /api/chat` — Send a question to the AI (standard chat).
- **RAG Chat:**
	- `POST /api/chat/RAG` — Query uploaded documents using Retrieval-Augmented Generation. The request body must be a JSON object: `{ "query": "your question" }`.

All API calls are handled in `src/app/services/api.service.ts`.

## UI Features

- Drag & drop or select PDF files to upload
- View a list of uploaded PDFs
- Chat interface for asking questions and receiving answers
- RAG chat mode for document-aware answers

## Accessibility & Best Practices

This project follows Angular and TypeScript best practices as described in `AGENTS.md`.

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
