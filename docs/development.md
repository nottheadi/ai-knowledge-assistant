# Development Guide

Complete guide for setting up a local development environment and development workflow.

---

## 🚀 Local Development Setup

### Prerequisites

```bash
# Check versions
python --version      # Should be 3.11+
node --version       # Should be 18+
npm --version        # Should be 9+
git --version        # Should be 2.x
```

### Full Setup (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/nottheadi/ai-knowledge-assistant.git
cd ai-knowledge-assistant

# 2. Run setup (installs all dependencies)
make setup

# 3. Create backend .env file
cd apps/backend
cp .env.example .env

# 4. Edit .env with your API keys
nano .env
# Set: GOOGLE_API_KEY, JWT_SECRET_KEY

# 5. Go back to root
cd ../..

# 6. Start both backend and frontend
make run
```

**Access the app**:
- Frontend: http://localhost:4200
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 💻 Backend Development

### Backend-Only Setup

```bash
cd apps/backend

# Install deps
make backend-setup

# Create config
cp .env.example .env
# Edit .env

# Run development server
make backend-run

# Or manually
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Project Structure

```
apps/backend/
├── app/
│   ├── main.py                    # FastAPI app setup
│   ├── config.py                  # JWT, rate limiting
│   ├── exceptions.py              # Custom exceptions
│   ├── routes/                    # Endpoints
│   │   ├── auth.py               # Login
│   │   └── chat.py               # Chat endpoints
│   ├── services/                  # Business logic
│   │   ├── llm.py                # Gemini integration
│   │   ├── memory.py             # Chat memory
│   │   └── user_service.py       # User auth
│   └── rag/                       # RAG pipeline
│       ├── loader.py             # PDF loading
│       ├── splitter.py           # Chunking
│       ├── embedder.py           # Embeddings
│       ├── vectorstore.py        # ChromaDB
│       ├── retriever.py          # Retrieval
│       ├── pipeline.py           # Processing
│       └── rag_chain.py          # Orchestration
├── tests/                         # Test files
├── requirements.txt               # Dependencies
└── .env                          # Configuration
```

### Code Style & Quality

```bash
# Format code
make backend-format
# Or: black apps/backend/app && isort apps/backend/app

# Lint
make backend-lint
# Or: flake8 apps/backend/app

# Run tests
make backend-test
# Or: pytest apps/backend/tests -v
```

### Adding a New Endpoint

1. **Create route** in `app/routes/`:
```python
from fastapi import APIRouter, Depends
from app.config import verify_jwt_token

router = APIRouter()

@router.post("/new-endpoint")
async def new_endpoint(req: RequestModel, token: dict = Depends(verify_jwt_token)):
    # Implementation
    return {"result": "..."}
```

2. **Add to main.py**:
```python
from app.routes import new_route
app.include_router(new_route.router, tags=["Feature"], prefix="/api")
```

3. **Test it**:
```bash
curl -X POST http://localhost:8000/api/new-endpoint \
  -H "Authorization: Bearer TOKEN"
```

### Database Migrations (Future)

When migrating from JSON to PostgreSQL:

```bash
# Install SQLAlchemy
pip install sqlalchemy

# Create migration
alembic init migrations
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```

---

## 🎨 Frontend Development

### Frontend-Only Setup

```bash
cd apps/frontend

# Install deps
npm install

# Run dev server
npm start
# or: make frontend-run
```

**Access app**: http://localhost:4200

### Project Structure

```
apps/frontend/src/app/
├── app.ts                         # Root component
├── app.routes.ts                  # Routes
├── app.config.ts                  # HTTP setup
├── core/
│   ├── services/
│   │   ├── api.service.ts        # API calls
│   │   ├── auth.service.ts       # JWT management
│   │   └── theme.service.ts      # Dark/light mode
│   ├── guards/
│   │   └── auth.guard.ts         # Route protection
│   └── interceptors/
│       └── auth.interceptor.ts   # JWT injection
├── features/
│   ├── auth/
│   │   └── pages/login/          # Login component
│   ├── chat/
│   │   ├── components/           # UI components
│   │   ├── models/               # Types
│   │   └── services/             # Chat logic
│   └── knowledge-base/
│       ├── components/           # KnowledgeBase UI
│       └── models/               # File types
└── environments/
    ├── environment.ts            # Dev config
    └── environment.prod.ts       # Prod config
```

### Code Style & Quality

```bash
# Lint TypeScript
npm run lint
# Or: npx eslint "src/**/*.ts"

# Format code
npm run format
# Or: npx prettier --write "src/**/*.ts"

# Run tests
npm test
# Or: ng test --watch

# Build production
npm run build
```

### Angular Best Practices

✅ **Do's**:
- Use standalone components
- Use RxJS `takeUntilDestroyed()` operator
- Use Change Detection Strategy: OnPush
- Use typed Observables
- Use Angular signals for state
- Use Dependency Injection

❌ **Don'ts**:
- Don't use `any` types (use proper types)
- Don't subscribe without unsubscribing
- Don't put logic in templates
- Don't create components without strong typing
- Don't use default change detection

### Adding a New Component

1. **Generate component**:
```bash
ng generate component features/chat/components/my-component
```

2. **Create template** (my-component.component.html):
```html
<div class="component">
  <p>{{ message }}</p>
</div>
```

3. **Create component logic** (my-component.component.ts):
```typescript
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-my-component',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './my-component.component.html',
  styleUrl: './my-component.component.css'
})
export class MyComponentComponent {
  @Input() message = '';
}
```

4. **Add to parent component**:
```typescript
import { MyComponentComponent } from './my-component/my-component.component';

@Component({
  imports: [MyComponentComponent],
  // ...
})
export class ParentComponent {}
```

### Creating a New Service

```bash
ng generate service core/services/my-service
```

```typescript
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class MyService {
  constructor(private http: HttpClient) {}

  getData() {
    return this.http.get('/api/data');
  }
}
```

---

## 🔄 Common Development Workflows

### Developing a New Feature

1. **Create feature branch**:
```bash
git checkout -b feature/my-feature
```

2. **Implement feature** (backend & frontend in parallel):
```bash
# Terminal 1: Backend
make backend-run

# Terminal 2: Frontend
make frontend-run
```

3. **Test locally**:
```bash
# Backend tests
make backend-test

# Frontend tests
npm test
```

4. **Commit changes**:
```bash
git add .
git commit -m "feat: add my new feature"
```

5. **Push and create PR**:
```bash
git push origin feature/my-feature
# Create PR on GitHub
```

### Debugging

#### Backend Debugging

```bash
# Add breakpoints in VSCode
# Run with debugpy
python -m debugpy --listen 5678 -m uvicorn app.main:app --reload
```

In VSCode, add to `.vscode/launch.json`:
```json
{
  "name": "Python: FastAPI",
  "type": "python",
  "request": "attach",
  "port": 5678
}
```

#### Frontend Debugging

```bash
# Chrome DevTools
# Open http://localhost:4200
# F12 → Sources tab
# Set breakpoints
```

Or use VSCode debugger:
```json
{
  "name": "ng serve",
  "type": "chrome",
  "request": "launch",
  "url": "http://localhost:4200",
  "webRoot": "${workspaceFolder}",
  "sourceMaps": true
}
```

### Testing Workflow

```bash
# Run all tests with file watching
make backend-test
npm test

# Run specific test
pytest tests/test_routes_chat.py::test_chat_rag -v
npm test -- --include='**/login.component.spec.ts'

# Generate coverage report
pytest --cov=app tests/
ng test --code-coverage
```

---

## 🐛 Debugging Common Issues

### Backend Won't Start

```bash
# Error: Address already in use
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
# Or use different port
uvicorn app.main:app --port 8001

# Error: ModuleNotFoundError
pip install -r requirements.txt

# Error: GOOGLE_API_KEY not found
cat apps/backend/.env  # Check if set
# Add to .env if missing
```

### Frontend Won't Build

```bash
# Clear cache
rm -rf .angular dist node_modules
npm install
npm start

# Port 4200 in use
ng serve --port 4201

# Build errors
npm run lint  # Find lint errors
npm run format
```

### API Connection Issues

```bash
# Check backend is running
curl http://localhost:8000/

# Check CORS
curl -H "Origin: http://localhost:4200" \
  -H "Access-Control-Request-Method: POST" \
  http://localhost:8000/api/chat

# Check environment config
cat apps/frontend/src/environments/environment.ts
# Should have: apiBaseUrl: 'http://localhost:8000'
```

---

## 📚 Development Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Angular Docs](https://angular.io/docs)
- [RxJS Docs](https://rxjs.dev/)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Tailwind CSS](https://tailwindcss.com/docs)

---

## 🔧 Editor Setup

### VSCode Extensions

Recommended extensions:

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "charliermarsh.ruff",
    "Angular.ng-template",
    "esbenp.prettier-vscode",
    "dbaeumer.vscode-eslint",
    "bradlc.vscode-tailwindcss"
  ]
}
```

### VSCode Settings

```json
{
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  }
}
```

---

## 📊 Key Commands Reference

| Command | Purpose |
|---------|---------|
| `make setup` | Install all dependencies |
| `make run` | Start both backend and frontend |
| `make backend-run` | Start backend only |
| `make frontend-run` | Start frontend only |
| `make backend-test` | Run backend tests |
| `make backend-lint` | Lint backend code |
| `make backend-format` | Format backend code |
| `make frontend-lint` | Lint frontend code |
| `make frontend-format` | Format frontend code |
| `make clean` | Remove build artifacts |
| `make stop` | Stop running processes |

---

**Last Updated**: March 29, 2026
**Status**: Complete ✅
