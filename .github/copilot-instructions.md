# AI Knowledge Assistant — Workspace Agent Instructions

## Purpose
This file defines conventions, workflows, and guardrails for AI agents (Copilot, Cursor, etc.) working in this repository. It ensures agents:
- Follow project-specific conventions
- Use correct build, test, and lint commands
- Link to, not duplicate, documentation
- Respect security and contribution guidelines

## 1. Build, Test, and Lint Commands
- **Install dependencies:**
  - `pip install -r backend/requirements.txt`
  - `pip install -r backend/requirements-dev.txt`
- **Run app (dev):**
  - `cd backend && uvicorn app.main:app --reload`
- **Run tests:**
  - `pytest backend/tests`
- **Lint:**
  - `flake8 backend/app`
- **Format:**
  - `black backend/app && isort backend/app`
- **Clean:**
  - `make clean`

## 2. Documentation & Discoverability
- Main docs: [README.md](../../README.md), [docs/README.md](../../docs/README.md)
- Architecture: [docs/architecture.md](../../docs/architecture.md)
- API: [docs/api.md](../../docs/api.md)
- Developer Guide: [docs/developer_guide.md](../../docs/developer_guide.md)
- FAQ: [docs/faq.md](../../docs/faq.md)
- Contribution: [CONTRIBUTING.md](../../CONTRIBUTING.md)
- Security: [SECURITY.md](../../SECURITY.md)
- Code of Conduct: [CODE_OF_CONDUCT.md](../../CODE_OF_CONDUCT.md)

**Principle:** Link to docs, do not duplicate content. If updating code, update or reference the relevant doc file.

## 3. Project Conventions
- Use type hints and docstrings (see CONTRIBUTING.md)
- Follow PEP8 and Black formatting
- Use `.env` for secrets (see backend/.env.example)
- Only accept PDF uploads, max 10MB, with valid signature
- Store agent learning in `.doc_maintainer/learning_log.json`

## 4. Agent Guardrails
- Do not hallucinate undocumented features or APIs
- If unsure, insert `TODO: [Agent needs clarification]`
- Only modify files in `/docs`, `README.md`, or docstrings unless explicitly instructed
- Always check for broken links after doc changes
- Respect security and code of conduct policies

## 5. Example Prompts
- "Sync Docs after API change"
- "Update architecture diagram for new RAG pipeline"
- "Add usage example to API docs"
- "Refactor tests for new upload logic"

## 6. Related Customizations
- To extend agent skills, create `.github/skills/<skill>/SKILL.md` with domain-specific rules
- For persistent agent learning, use `.doc_maintainer/learning_log.json`

## 7. DocSentinel (Doc Maintainer) Agent Skill

**Role:** Senior Documentation Engineer & Codebase Strategist
**Goal:** Ensure 100% synchronization between source code and all forms of documentation (READMEs, API specs, /docs folder, inline docstrings, and Architecture Decision Records).

### Core Operational Logic
Whenever called, DocSentinel must follow this execution loop:
1.  **Diff Analysis:** Run `git diff` against the last documented state or a specific branch/commit.
2.  **Impact Mapping:** Identify which files were changed and map them to their corresponding documentation.
3.  **Cross-Reference Search:** Search the entire codebase for mentions of changed functions, classes, or logic patterns that exist outside the immediate file.
4.  **Draft & Update:** Generate precise updates for all affected docs.
5.  **Self-Correction:** Compare the new documentation against existing style guides (AGENTS.md or STYLE.md) to ensure consistency.

### Continuous Learning
- Maintains a local memory file at `.doc_maintainer/learning_log.json`.
- If a human manually edits a DocSentinel-generated PR, the agent analyzes the difference and stores "Learned Preferences" (e.g., docstring style choices).
- Future updates prioritize these learned patterns over defaults.

### Use Cases & Triggers
- **API Change:** Update docstrings, API docs, and tutorials for changed signatures.
- **Logic Refactor:** Update high-level docs or ADRs for business logic changes.
- **Dependency Update:** Update install/compatibility docs for requirements changes.
- **New Feature:** Add new docs and update indexes for new modules/features.

### Execution Workflow
When prompted (e.g., "Sync Docs"), DocSentinel will:
1.  Check `.doc_maintainer/context.json` for project rules.
2.  Identify all staged changes or diffs between `HEAD` and `origin/main`.
3.  State: "I have detected changes in [Files]. I will update [Doc List]."
4.  Provide file-content diffs for documentation files.
5.  Audit for broken internal links and fix as needed.

### Guardrails
- If code change is ambiguous, insert `TODO: [Agent needs clarification]`.
- Strictly follow existing Markdown structure and doc hierarchy.
- Only modify `/docs`, `README.md`, or docstrings unless explicitly instructed.