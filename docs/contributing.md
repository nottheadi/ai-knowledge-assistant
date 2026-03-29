# Contributing Guide

Thank you for your interest in contributing to the AI Knowledge Assistant! This document provides guidelines and instructions for contributing.

---

## 🤝 Ways to Contribute

- **Code**: Fix bugs, add features, improve performance
- **Documentation**: Improve guides, add examples, clarify concepts
- **Testing**: Add tests, improve test coverage, find edge cases
- **Issues**: Report bugs, suggest features, ask questions
- **Reviews**: Review pull requests, provide feedback

---

## 🚀 Getting Started

### 1. Fork the Repository

```bash
# Go to GitHub and click "Fork"
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ai-knowledge-assistant.git
cd ai-knowledge-assistant

# Add upstream remote
git remote add upstream https://github.com/nottheadi/ai-knowledge-assistant.git
```

### 2. Setup Development Environment

```bash
# Install all dependencies
make setup

# Setup backend
cd apps/backend
cp .env.example .env
# Edit .env with your API keys

# Go back to root
cd ../..
```

### 3. Create a Branch

```bash
# Update from upstream
git fetch upstream
git checkout upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
# or for bugs:
git checkout -b fix/bug-description
# or for docs:
git checkout -b docs/documentation-topic
```

---

## 📋 Branch Naming Convention

Use descriptive branch names:

| Type | Example |
|------|---------|
| Feature | `feature/user-authentication` |
| Bug Fix | `fix/api-error-handling` |
| Documentation | `docs/setup-guide` |
| Refactor | `refactor/component-organization` |
| Tests | `test/increase-coverage` |

---

## 💻 Development Workflow

### Making Changes

```bash
# Start development servers
make run
# Backend: http://localhost:8000
# Frontend: http://localhost:4200

# Make your changes
# Your code editor will auto-reload

# Test your changes locally
make backend-test
npm test

# Run linting
make backend-lint
make frontend-lint

# Format code
make backend-format
make frontend-format
```

### Code Quality Standards

#### Backend (Python)

✅ **Required**:
- All functions must have docstrings
- Type hints required for function arguments
- Black formatting (88 char line length)
- No unused imports
- Error handling implemented
- Tests for new functionality

❌ **Avoid**:
- `print()` statements (use logging)
- Global variables
- Long functions (>30 lines)
- Magic numbers without explanation

Example:
```python
def process_document(file_path: str) -> dict:
    """Process PDF document and return metadata.

    Args:
        file_path: Path to PDF file

    Returns:
        Dictionary with processed document info

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If not a valid PDF
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Implementation
    return {"status": "processed"}
```

#### Frontend (TypeScript)

✅ **Required**:
- Strong typing (no `any` except in edge cases)
- Angular best practices
- Standalone components
- RxJS proper unsubscription
- AccessibilityFeatures (ARIA labels, semantic HTML)
- OnPush change detection strategy
- Tests for components

❌ **Avoid**:
- `any` types
- Long component files (>300 lines)
- Deep component nesting
- Code duplication
- Material Design not followed

Example:
```typescript
@Component({
  selector: 'app-my-component',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './my-component.component.html',
  styleUrl: './my-component.component.css',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class MyComponent implements OnInit {
  @Input() data: string = '';

  protected readonly vm$ = this.service.data$;

  constructor(
    private service: MyService,
    private destroyRef: DestroyRef
  ) {}

  ngOnInit(): void {
    this.service.load$()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(data => console.log(data));
  }
}
```

---

## ✅ Testing Requirements

### Backend Tests

```bash
# Run tests with coverage
pytest tests/ --cov=app

# Run specific test
pytest tests/test_routes_chat.py::test_chat_rag -v

# Test naming convention
# test_<function>_<scenario>.py
# Example: test_login_with_invalid_credentials
```

Example test:
```python
def test_chat_rag_with_valid_query(client, auth_headers):
    """Test RAG chat with valid query returns answer and sources."""
    response = client.post(
        "/api/chat/RAG",
        json={"query": "What is the document about?"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
```

### Frontend Tests

```bash
# Run tests
npm test -- --watch=false

# Run with coverage
ng test --code-coverage

# Test naming convention
# <component>.component.spec.ts
```

Example test:
```typescript
describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginComponent],
      providers: [
        { provide: AuthService, useValue: mockAuthService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should login with valid credentials', () => {
    // Test implementation
    expect(component.isLoading).toBe(false);
  });
});
```

---

## 📝 Git Commit Convention

Use clear, descriptive commit messages following this format:

```
<type>: <description>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding/updating tests
- `chore`: Build process, dependencies

### Examples

```bash
# Feature
git commit -m "feat: add JWT authentication for protected routes

- Implement login endpoint POST /api/auth/login
- Add JWT token generation and validation
- Protect chat endpoints with auth guard
- Store tokens in localStorage on frontend"

# Bug fix
git commit -m "fix: prevent null pointer in RAG chain

Fix issue where undefined documents caused pipeline to crash.
Add validation for empty retrieval results."

# Documentation
git commit -m "docs: add backend setup guide

include instructions for:
- installing dependencies
- configuring .env
- running local dev server"
```

---

## 📤 Creating a Pull Request

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No console errors/warnings
- [ ] Changes are focused (not too many things at once)

### Create PR on GitHub

1. **Push your branch**:
```bash
git push origin feature/your-feature-name
```

2. **Create pull request** on GitHub with:
   - Clear title (e.g., "Add user authentication")
   - Description of changes
   - Link to related issues (e.g., "Fixes #123")
   - Screenshots if UI changes
   - Testing suggestions

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update

## Changes
- Change 1
- Change 2

## Testing Done
- Tested locally with X scenario
- All tests passing

## Screenshots (if applicable)
[Add screenshots]

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No breaking changes
```

---

## 🔍 Code Review Process

### What Reviewers Look For

- **Code Quality**: Follows patterns, no duplication
- **Testing**: Tests cover new functionality
- **Documentation**: Changes documented
- **Performance**: No unnecessary queries/renders
- **Security**: No vulnerabilities introduced
- **Compatibility**: No breaking changes

### Responding to Feedback

- Address all comments
- Re-request review after changes
- Use "conversation resolved" to close discussions
- Don't force-push unless requested

---

## 🐛 Reporting Bugs

Use GitHub Issues:

**Title**: Descriptive bug summary

**Description**:
```markdown
## Environment
- Python/Node version
- OS
- Other relevant info

## Steps to Reproduce
1. Step one
2. Step two
3. Expected vs actual result

## Screenshots/Logs
[Add logs, screenshots, etc]

## Possible Solutions
[Optional: your ideas for fixing it]
```

---

## 🎯 Feature Requests

**Title**: Feature description

**Description**:
```markdown
## Problem
What problem does this solve?

## Solution
How should it work?

## Use Cases
Who would benefit?

## Alternative Solutions
Are there other approaches?
```

---

## 📚 Documentation Guidelines

### Writing Docs

- Use clear, concise language
- Add code examples
- Reference related docs
- Update table of contents
- Include both happy path and errors

### File Naming

- **Guides**: lowercase with hyphens (setup-guide.md)
- **API Docs**: descriptive (api-reference.md)
- **Architecture**: specific domains (authentication.md)

### Markdown Formatting

```markdown
# Heading 1

## Heading 2

### Heading 3

**Bold text**
*Italic text*

[Link text](http://example.com)

- List item 1
- List item 2

1. Numbered item
2. Another item

> Quote or note

\`\`\`python
# Code block
\`\`\`

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
```

---

## ⚠️ Important Notes

### Do's ✅

- Be respectful and professional
- Ask questions if unclear
- Use descriptive titles/descriptions
- Keep commits focused and small
- Update related documentation
- Add tests for new features

### Don'ts ❌

- Don't submit large PRs without discussion
- Don't commit directly to main branch
- Don't ignore failing tests
- Don't commit secrets/API keys
- Don't change unrelated code
- Don't force-push without consent

---

## 🔒 Security

If you discover a security vulnerability:

1. **Do NOT** open a public issue
2. **Email**: security@example.com (use actual email)
3. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

---

## 💬 Getting Help

- **Questions**: Use GitHub Discussions
- **Issues**: Check existing issues before creating new
- **Chat**: [Discord/Slack link if applicable]
- **Docs**: Check `/docs` folder first

---

## 📊 Development Roadmap

See [GitHub Projects](https://github.com/nottheadi/ai-knowledge-assistant/projects) for planned features and current progress.

---

## 🏆 Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Thanked in project highlights

---

## 📖 Additional Resources

- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Effective Pull Requests](https://github.blog/2015-01-21-how-to-write-the-perfect-pull-request/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Angular Style Guide](https://angular.io/guide/styleguide)
- [PEP 8 Python Style](https://www.python.org/dev/peps/pep-0008/)

---

## 📝 License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

---

Thank you for contributing! 🎉

**Questions?** Open an issue or contact maintainers.

---

**Last Updated**: March 29, 2026
**Status**: Active ✅
