# 🚀 Quick Reference Guide

Your fast reference for common tasks.

---

## ⚡ 5-Minute Quick Start

```bash
# 1. Clone
git clone https://github.com/nottheadi/ai-knowledge-assistant.git
cd ai-knowledge-assistant

# 2. Setup (auto-installs dependencies)
make setup

# 3. Configure backend
cd apps/backend
cp .env.example .env
# Edit .env: set GOOGLE_API_KEY and JWT_SECRET_KEY
cd ../..

# 4. Run (starts frontend on 4200, backend on 8000)
make run

# 5. Access
# Open: http://localhost:4200 (login: admin/password123)
# API Docs: http://localhost:8000/docs
```

---

## 📖 Documentation Quick Links

| Need | Link | Time |
|------|------|------|
| **Overview** | [README.md](README.md) | 5 min |
| **Feel lost?** | [Docs Hub](docs/README.md) | 2 min |
| **Architecture** | [Architecture](docs/architecture.md) | 20 min |
| **API Calls** | [API Ref](docs/api.md) | 10 min |
| **Setup Backend** | [Backend](docs/backend.md) | 15 min |
| **Setup Frontend** | [Frontend](docs/frontend.md) | 15 min |
| **Development** | [Dev Guide](docs/development.md) | 20 min |
| **Deploy** | [Deployment](docs/deployment.md) | 30 min |
| **Contribute** | [Contributing](docs/contributing.md) | 15 min |

---

## ⌨️ Essential Commands

### Setup & Running

```bash
# First time setup
make setup

# Run everything (frontend + backend)
make run

# Backend only
make backend-run

# Frontend only
make frontend-run

# Stop everything
make stop

# Clean build artifacts
make clean
```

### Testing

```bash
# Backend tests
make backend-test

# Frontend tests
npm test

# With coverage
pytest --cov=app tests/
```

### Code Quality

```bash
# Backend
make backend-lint      # Check style
make backend-format    # Auto-format

# Frontend
npm run lint           # Check style
npm run format         # Auto-format
```

### Building

```bash
# Frontend production build
npm run build

# Backend testing
pytest tests/ -v
```

---

## 🔐 Authentication

### Login (Development)
```
Username: admin
Password: password123
```

### Get JWT Token
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'
```

### Use Token
```bash
TOKEN="your-token-here"
curl -X POST http://localhost:8000/api/chat/RAG \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"Your question"}'
```

---

## 🔗 API Quick Reference

### Chat Endpoints

**Direct Chat** (no documents)
```bash
POST /api/chat
Body: {"query": "What is machine learning?"}
```

**RAG Chat** (with documents)
```bash
POST /api/chat/RAG
Body: {"query": "Summarize the document"}
Response: {answer, sources}
```

### File Endpoints

**Upload**
```bash
POST /api/upload
Form-data: file=document.pdf
```

**List Files**
```bash
GET /api/uploads
Response: {files: [...]}
```

**Delete File**
```bash
DELETE /api/uploads/filename.pdf
```

---

## 🛠️ Common Tasks

### I want to...

**...add a new API endpoint**
1. Create route in `apps/backend/app/routes/`
2. Define request model with validation
3. Add to `app/main.py`
4. Add tests
5. Document in [API ref](docs/api.md)

See: [Backend Setup](docs/backend.md#adding-a-new-endpoint)

**...add a new component**
1. Generate with `ng generate component`
2. Implement component logic
3. Add to parent imports
4. Write tests
5. Document in [Frontend Setup](docs/frontend.md)

See: [Frontend Setup](docs/frontend.md#creating-a-new-component)

**...deploy to production**
1. Read [Deployment Guide](docs/deployment.md)
2. Choose option (Docker recommended)
3. Follow deployment steps
4. Setup monitoring
5. Backup data

See: [Deployment Guide](docs/deployment.md)

**...contribute code**
1. Fork repo
2. `git checkout -b feature/name`
3. Make changes
4. Run tests: `make backend-test && npm test`
5. Create PR
6. Address feedback

See: [Contributing Guide](docs/contributing.md)

**...fix a bug**
1. Find issue
2. Create branch: `git checkout -b fix/bug-name`
3. Make fix
4. Add/update tests
5. Commit with clear message
6. Create PR

See: [Contributing Guide](docs/contributing.md#reporting-bugs)

---

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Port 8000 in use?
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Missing API key?
echo "GOOGLE_API_KEY=your-key" >> apps/backend/.env

# Missing dependencies?
pip install -r apps/backend/requirements.txt
```

### Frontend Won't Load
```bash
# Port 4200 in use?
ng serve --port 4201

# Module errors?
rm -rf node_modules package-lock.json
npm install

# Check backend is running
curl http://localhost:8000/
```

### Can't Login
```bash
# Check .env has JWT_SECRET_KEY
cat apps/backend/.env

# Test auth manually
curl -X POST http://localhost:8000/api/auth/login \
  -d '{"username":"admin","password":"password123"}'

# Check default credentials
# Username: admin
# Password: password123
```

### API Errors
- **401 Unauthorized**: Token missing/expired - login again
- **422 Unprocessable**: Invalid request format - check body
- **429 Too Many Requests**: Rate limited - wait 1 minute
- **500 Server Error**: Check backend logs - `journalctl -f`

See: [API Reference](docs/api.md#-error-handling) for all error codes

---

## 📁 Key Files

### Backend
```
apps/backend/
├── app/main.py         ← FastAPI setup
├── app/config.py       ← JWT & rate limiting
├── app/routes/         ← API endpoints
├── app/services/       ← Business logic
├── app/rag/            ← RAG pipeline
└── .env                ← Configuration
```

### Frontend
```
apps/frontend/src/app/
├── app.ts              ← Root component
├── core/services/      ← API, Auth, Theme
├── core/guards/        ← Auth protection
├── features/auth/      ← Login page
└── features/chat/      ← Chat interface
```

---

## 🔧 Environment Variables

### Backend (.env)

**Required**:
```env
GOOGLE_API_KEY=your-api-key
JWT_SECRET_KEY=long-random-secret-min-32-chars
```

**Optional**:
```env
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
API_HOST=0.0.0.0
API_PORT=8000
```

### Frontend

**Development** (`environment.ts`):
```typescript
apiBaseUrl: 'http://localhost:8000'
```

**Production** (`environment.prod.ts`):
```typescript
apiBaseUrl: 'https://api.yourdomain.com'
```

---

## 📊 Directory Structure

```
ai-knowledge-assistant/
├── README.md                ← Start here
├── docs/
│   ├── README.md           ← Doc hub
│   ├── api.md              ← API reference
│   ├── architecture.md      ← System design
│   ├── backend.md          ← Backend guide
│   ├── frontend.md         ← Frontend guide
│   ├── development.md      ← Dev workflow
│   ├── deployment.md       ← Deployment
│   └── contributing.md     ← Contributing
├── apps/
│   ├── backend/            ← FastAPI
│   └── frontend/           ← Angular
├── Makefile                ← Commands
└── DOCUMENTATION_COMPLETE.md ← Completion summary
```

---

## 🔑 Keyboard Shortcuts

### VS Code
```
Ctrl+` = Open terminal
Ctrl+/ = Toggle comment
Ctrl+Shift+F = Find in files
Ctrl+P = Quick file open
F12 = Go to definition
```

### Chrome DevTools
```
F12 = Open DevTools
Ctrl+Shift+I = Open DevTools
Ctrl+Shift+C = Inspect element
Ctrl+Shift+J = Console
```

---

## 🎓 Learning Paths

### Beginner (1-2 hours)
1. Read [README.md](README.md) (10 min)
2. Run `make run` and explore app (15 min)
3. Read [Architecture](docs/architecture.md) overview (20 min)
4. Try an API call from [API Ref](docs/api.md) (10 min)

### Intermediate (3-4 hours)
1. Follow [Backend Setup](docs/backend.md) completely
2. Follow [Frontend Setup](docs/frontend.md) completely
3. Read [Development Guide](docs/development.md)
4. Make a small code change and test

### Advanced (full day)
1. Study [Architecture Overview](docs/architecture.md) deeply
2. Study [RAG Pipeline](docs/backend.md#-rag-pipeline-details)
3. Read [Deployment Guide](docs/deployment.md)
4. Plan system improvements

---

## 💡 Pro Tips

1. **Use Makefile** - `make` shows all available commands
2. **Check logs** - `tail -f` for backend/frontend logs
3. **Use VS Code** - Install recommended extensions
4. **Test early** - Run tests before committing
5. **Read docs** - Most answers are in `/docs`
6. **Check examples** - Refer to existing code/tests
7. **Ask in issues** - Check closed issues first
8. **Keep notes** - Document what you learn

---

## 🔗 Important Links

- **GitHub**: https://github.com/nottheadi/ai-knowledge-assistant
- **Local Frontend**: http://localhost:4200
- **Local API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

---

## 📞 Getting Help

| Issue | Solution |
|-------|----------|
| **Setup problem** | Check [Development Guide](docs/development.md) |
| **API question** | Check [API Reference](docs/api.md) |
| **Architecture question** | Check [Architecture](docs/architecture.md) |
| **Not in docs** | Open GitHub Issue |
| **Security issue** | Email maintainers (see SECURITY.md) |

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Setup backend | 10 min |
| Setup frontend | 10 min |
| Run locally | 5 min |
| First API call | 5 min |
| Read architecture | 20 min |
| Read full docs | 3-4 hours |
| Deploy to production | 1-2 hours |
| Onboard new developer | 1 hour |

---

## ✨ Next Steps

1. **Read**: [README.md](README.md) (everyone)
2. **Setup**: Run `make setup && make run`
3. **Explore**: Check [Docs Hub](docs/README.md)
4. **Learn**: Read docs for your role
5. **Build**: Start developing!

---

**Questions?** Check the [Docs Hub](docs/README.md) or open an issue on GitHub.

**Version**: 1.0.0
**Last Updated**: March 29, 2026
