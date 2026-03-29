# Frontend Documentation

## Overview

The frontend is a modern, single-page application (SPA) built with Angular that provides an intuitive interface for uploading documents and querying them using RAG-powered AI.

**Stack**: Angular 21+ | TypeScript 5.9+ | Tailwind CSS | RxJS | Marked

---

## 🏗️ Architecture

### Component Structure

```
apps/frontend/src/app/
├── app.ts                      # Root component
├── app.html                    # Root template
├── core/
│   ├── services/
│   │   ├── api.service.ts      # HTTP requests + RAG API
│   │   ├── auth.service.ts     # JWT token management
│   │   └── theme.service.ts    # Dark/Light mode
│   ├── guards/
│   │   └── auth.guard.ts       # Route protection
│   └── interceptors/
│       └── auth.interceptor.ts # JWT token injection
├── features/
│   ├── auth/
│   │   └── pages/
│   │       └── login/          # Login page
│   │           ├── login.component.ts
│   │           ├── login.component.html
│   │           └── login.component.css
│   ├── chat/
│   │   ├── components/
│   │   │   ├── chat-input/     # Message input
│   │   │   ├── message-list/   # Chat history
│   │   │   └── message-bubble/ # Individual message
│   │   ├── models/
│   │   │   └── message.model.ts
│   │   └── services/
│   │       └── chat.service.ts (suggested)
│   └── knowledge-base/
│       ├── components/
│       │   └── file-management/ (suggested)
│       └── models/
│           └── uploaded-file.model.ts
├── app.routes.ts               # Route definitions
├── app.config.ts               # HTTP providers & interceptors
└── environments/
    ├── environment.ts          # Development config
    └── environment.prod.ts     # Production config
```

### Data Flow

```
User Input
    ↓
[Components] → User action
    ↓
[Services] → HTTP Request to Backend
    ↓
[API Service] → Backend API
    ↓
[RxJS Observables] → Response handling
    ↓
[Components] → Update UI
    ↓
Display to User
```

---

## 📦 Installation

### 1. Prerequisites

```bash
node --version  # Should be 18+
npm --version   # Should be 9+
```

### 2. Install Dependencies

```bash
cd apps/frontend

# Install npm packages
npm install

# Verify installation
npm list @angular/core
```

### 3. Configure Environment

**Development** (`src/environments/environment.ts`):
```typescript
export const environment = {
  production: false,
  apiBaseUrl: 'http://localhost:8000'
};
```

**Production** (`src/environments/environment.prod.ts`):
```typescript
export const environment = {
  production: true,
  apiBaseUrl: 'https://api.yourdomain.com'
};
```

---

## 🚀 Running the Frontend

### Development Mode

```bash
cd apps/frontend

# Start dev server with auto-reload
npm start

# Or using make command
make frontend-run
```

The application will be available at: **http://localhost:4200**

### Production Build

```bash
# Build optimized bundle
npm run build

# Build uses environment.prod.ts automatically
# Output in dist/apps/frontend/
```

### Serve Production Build Locally

```bash
# Install local web server
npm install -g http-server

# Serve the build
cd dist/apps/frontend
http-server
```

---

## 🔐 Authentication

### Login Flow

1. **User lands on `/login`** (redirected if not authenticated)
2. **Enters credentials** (default: admin / password123)
3. **Frontend posts** to `POST /api/auth/login`
4. **Backend returns** JWT token
5. **Frontend stores** token in `localStorage`
6. **Interceptor adds** token to all subsequent requests
7. **Redirects to** `/chat`

### JWT Token Management (`core/services/auth.service.ts`)

```typescript
export class AuthService {
  login(username: string, password: string): Observable<LoginResponse> {
    // Posts to /api/auth/login
    // Stores token in localStorage
    // Returns user info
  }

  logout(): void {
    // Clears localStorage
    // Removes token from memory
  }

  getToken(): string | null {
    // Returns stored JWT token
  }

  isAuthenticated(): boolean {
    // Checks if token exists and is valid
  }
}
```

### Auth Guard (`core/guards/auth.guard.ts`)

Protects `/chat` route:
- If authenticated: allows navigation
- If not authenticated: redirects to `/login`

### Auth Interceptor (`core/interceptors/auth.interceptor.ts`)

Adds JWT token to every HTTP request:
```typescript
Authorization: Bearer eyJhbGc...
```

---

## 📱 Components

### Root Component (`app.ts`)

**Responsibilities**:
- Chat message management
- File upload handling
- Loading states
- Theme switching
- Logout functionality

**Key Methods**:
| Method | Purpose |
|--------|---------|
| `send()` | Send chat message via RAG |
| `upload()` | Upload PDF file |
| `deleteFile()` | Delete uploaded file |
| `logout()` | Clear token & redirect |
| `fetchUploadedFiles()` | Load file list |

### Login Component (`features/auth/pages/login/`)

**Template Features**:
- Username input field
- Password input field
- Login button with loading state
- Error message display
- Helpful default credentials for dev

**Method**:
```typescript
login(): void {
  // Posts to backend
  // Stores token
  // Navigates to chat
}
```

### Chat Components

#### **ChatInputComponent** (`features/chat/components/chat-input/`)
- Text input for messages
- Submit button
- File upload trigger
- Drag-and-drop area for files

#### **MessageListComponent** (`features/chat/components/message-list/`)
- Displays chat history
- Auto-scrolls to latest message
- Shows loading indicator
- Formats markdown responses

#### **MessageBubbleComponent** (`features/chat/components/message-bubble/`)
- Individual message display
- User/AI distinction
- Markdown rendering (via `marked`)
- Source attribution display

---

## 🎨 Styling

### Tailwind CSS

The project uses Tailwind CSS for styling:

```bash
# Config: tailwind.config.ts
# CSS: src/styles.css
# Per-component: *.component.css
```

### Theme System (`core/services/theme.service.ts`)

Manages dark/light mode:
```typescript
export class ThemeService {
  isDarkMode = signal(false);

  toggleTheme(): void {
    // Switches dark/light
    // Persists to localStorage
    // Updates CSS variables
  }
}
```

**CSS Variables** (in root component):
```css
--color-bg-primary: #ffffff;  /* Light mode */
--color-text-primary: #000000;

/* Dark mode */
[data-theme="dark"] {
  --color-bg-primary: #1a1a1a;
  --color-text-primary: #ffffff;
}
```

---

## 🔄 Services

### API Service (`core/services/api.service.ts`)

Handles all backend communication:

```typescript
export class ApiService {
  baseUrl = `${environment.apiBaseUrl}/api`;

  // Authentication
  login(username: string, password: string): Observable<LoginResponse>

  // Chat
  chat(query: string): Observable<ChatResponse>
  chatRag(query: string): Observable<RagResponse>

  // Files
  uploadFile(file: File): Observable<UploadResponse>
  getUploadedFiles(): Observable<FileListResponse>
  deleteFile(fileName: string): Observable<DeleteResponse>
}
```

### Auth Service (`core/services/auth.service.ts`)

Token and user management:

```typescript
export class AuthService {
  login(username: string, password: string): Observable<LoginResponse>
  logout(): void
  getToken(): string | null
  isAuthenticated(): boolean
  getCurrentUser(): Observable<User | null>
}
```

### Theme Service (`core/services/theme.service.ts`)

Appearance preferences:

```typescript
export class ThemeService {
  isDarkMode = signal(false);
  toggleTheme(): void
  loadPreferences(): void
  savePreferences(): void
}
```

---

## 💾 Models & Types

### Message Model (`features/chat/models/message.model.ts`)

```typescript
export interface Message {
  sender: 'User' | 'AI';
  text: string;
  html?: SafeHtml;
  sources?: DocumentSource[];
  timestamp?: Date;
}
```

### Uploaded File Model (`features/knowledge-base/models/uploaded-file.model.ts`)

```typescript
export interface UploadedFile {
  name: string;
  status: 'uploaded' | 'uploading' | 'deleting';
  uploadedAt?: Date;
  size?: number;
}
```

### API Response Models

```typescript
interface LoginResponse {
  access_token: string;
  token_type: string;
  user: { id: string; username: string };
}

interface ChatResponse {
  response: string;
  error?: string;
}

interface RagResponse {
  answer: string;
  sources: DocumentSource[];
  error?: string;
}

interface DocumentSource {
  title: string;
  page: number;
  content: string;
}
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
npm test

# Run with watch mode
npm test -- --watch

# Run specific test file
npm test -- --include='**/login.component.spec.ts'
```

### Test Structure

```
src/app/
├── app.spec.ts
├── core/
│   ├── services/
│   │   ├── api.service.spec.ts
│   │   ├── auth.service.spec.ts
│   │   └── theme.service.spec.ts
│   └── guards/
│       └── auth.guard.spec.ts
└── features/
    ├── auth/
    │   └── pages/login/login.component.spec.ts
    └── chat/
        ├── components/
        │   ├── chat-input.component.spec.ts
        │   └── message-list.component.spec.ts
        └── services/
            └── chat.service.spec.ts
```

### Example Test

```typescript
describe('AuthService', () => {
  let service: AuthService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AuthService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should login and store token', () => {
    service.login('admin', 'password').subscribe();

    const req = httpMock.expectOne('/api/auth/login');
    req.flush({ access_token: 'test-token' });

    expect(service.getToken()).toBe('test-token');
  });
});
```

---

## 📊 Code Quality

### Linting

```bash
# Lint TypeScript files
npm run lint

# Or with eslint
npx eslint "src/**/*.ts"
```

### Formatting

```bash
# Format code with prettier
npm run format

# Or manually
npx prettier --write "src/**/*.{ts,html,css}"
```

### Build Optimization

```bash
# Check bundle size
npm run build -- --stats-json
npm install -g webpack-bundle-analyzer
webpack-bundle-analyzer dist/apps/frontend/browser/stats.json
```

---

## 🔧 Routing

### Routes (`app.routes.ts`)

```typescript
export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  {
    path: 'chat',
    component: App,
    canActivate: [authGuard]
  },
  { path: '', redirectTo: '/chat', pathMatch: 'full' },
  { path: '**', redirectTo: '/chat' }
];
```

**Navigation**:
- Unauthenticated users → `/login`
- Authenticated users → `/chat` (app shell)
- Default route → `/chat`

---

## 📱 Responsive Design

### Breakpoints

Using Tailwind CSS breakpoints:

| Breakpoint | Width | Class |
|-----------|-------|-------|
| Mobile | <640px | (no prefix) |
| Tablet | ≥640px | `sm:` |
| Desktop | ≥1024px | `lg:` |
| Wide | ≥1280px | `xl:` |

### Mobile Optimization

- Touch-friendly buttons (min 44px height)
- Responsive grid for file list
- Flexible chat interface
- Dynamic text sizing

---

## 🚀 Performance

### Optimizations Implemented

1. **OnPush Change Detection**
   ```typescript
   @Component({
     changeDetection: ChangeDetectionStrategy.OnPush
   })
   ```

2. **Lazy Loading**
   - Auth module loaded separately
   - Chat feature lazy-loaded after login

3. **Signal-Based Reactivity**
   - Using Angular signals for state
   - Automatic change detection

4. **RxJS Operators**
   - `shareReplay()`: Cache API responses
   - `debounceTime()`: Reduce API calls
   - `takeUntilDestroyed()`: Memory leak prevention

### Bundle Analysis

```bash
npm run build
npm run analyze  # Shows bundle size breakdown
```

---

## 🐛 Troubleshooting

### API Connection Issues

**Problem**: Cannot connect to backend
```bash
# Check backend is running
curl http://localhost:8000/

# Check environment config
cat src/environments/environment.ts

# Verify apiBaseUrl is correct
# Should be: http://localhost:8000 (development)
```

**Problem**: CORS error
```bash
# Frontend is trying to reach wrong backend
# Update environment.ts with correct URL
# Check backend CORS configuration

curl -H "Origin: http://localhost:4200" \
  http://localhost:8000/api/chat/RAG
```

### Authentication Issues

**Problem**: Login fails with 401
```bash
# Check credentials
# Default: admin / password123

# Verify backend JWT configuration
# Check .env has JWT_SECRET_KEY

# Try logging in with curl
curl -X POST http://localhost:8000/api/auth/login \
  -d '{"username":"admin","password":"password123"}'
```

**Problem**: Token expires on logout
```typescript
// The interceptor should handle this:
// 1. Catch 401 error
// 2. Clear localStorage
// 3. Redirect to /login
```

### Build Issues

**Problem**: Cannot find module errors
```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Problem**: CSS not applied
```bash
# Clear cache and rebuild
rm -rf .angular/ dist/
ng build
```

---

## 🔒 Security Best Practices

1. **Token Handling**
   - ✅ Stored in localStorage (XSS-vulnerable but simple)
   - ✅ Cleared on logout
   - ✅ Validated in auth guard

2. **Input Validation**
   - ✅ File type checking (PDF only)
   - ✅ File size validation (10MB max)
   - ✅ Query length validation (min 1, max 5000 chars)

3. **API Security**
   - ✅ HTTPS in production
   - ✅ JWT authentication on protected endpoints
   - ✅ Rate limiting (10 req/min)

4. **XSS Prevention**
   - ✅ Using `bypassSecurityTrustHtml()` carefully with `marked`
   - ✅ Sanitizing user inputs via DomSanitizer
   - ✅ Content Security Policy headers (on server)

---

## 📚 Dependencies

Key npm packages:

```json
{
  "@angular/core": "^21.2.0",
  "@angular/router": "^21.2.0",
  "@angular/forms": "^21.2.0",
  "@angular/platform-browser": "^21.2.0",
  "rxjs": "~7.8.0",
  "marked": "^17.0.5",
  "tailwindcss": "^4.1.12"
}
```

---

## 📖 Additional Resources

- [Angular Documentation](https://angular.io/docs)
- [RxJS Guide](https://rxjs.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Marked.js](https://marked.js.org/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

---

## 🎯 Future Improvements

- [ ] Extract ChatService for better separation of concerns
- [ ] Add comprehensive error handling with toast notifications
- [ ] Implement file preview before upload
- [ ] Add retry logic for failed requests
- [ ] Create TypeScript models for all API responses
- [ ] Add end-to-end tests with Cypress
- [ ] Implement service worker for offline support
- [ ] Add analytics tracking

---

**Last Updated**: March 29, 2026
**Status**: Production Ready ✅
