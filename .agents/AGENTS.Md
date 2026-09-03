# Project Context

**Melitrack** is a platform for monitoring, tracking, and classifying bees and insects using Machine Learning.
This repository is a monorepo containing the following components:

- **Backend API**: Main REST API in Python (FastAPI), PostgreSQL, and MongoDB (`backend/api/`).
- **Backend ML**: Machine Learning service with TensorFlow, FastAPI, and Celery + Redis (`backend/ml/`).
- **Frontend**: SPA web application in React with Vite and Tailwind CSS (`frontend/`).
- **Observability**: Docker Compose and Grafana/Loki/Alloy stack (`observability/`).

Before starting any task, read the code and configurations related to the module to be modified.

---

# Working Rules and Architecture

- **Incremental Steps**: Work in small, verifiable steps.
- **Strict Scope**: Implement ONLY what was requested. Do not add extra features.
- **Reusability**: Maximize the reuse of existing code. Do not rewrite working solutions.
- **Isolation**: Do not modify modules or files that are not directly related to the task.
- **Modular Design**:
  - `backend/api/apps/`: Routes, Pydantic schemas, and business logic for the main API resources.
  - `backend/ml/app/`: Inference tasks, Celery processing, and iNaturalist integration.
  - `frontend/src/`: React functional components, custom hooks, and centralized service calls.
- **Code Practices**:
  - **Python**: Use modern Python 3.12+ (`async/await`, complete type hints).
  - **JavaScript/TypeScript**: Use ES6+ / TypeScript with `async/await`. NEVER use `.then()/.catch()`.
- **Security**: Do not expose sensitive data (passwords, hashes, secret keys, tokens) in API responses or public repository files.
- **Language**: Write error messages, logs, code comments, and documentation in English.

---

# Workflow Before Code Changes

1. **Reading**: Read the code and architecture related to the task.
2. **Patterns**: Identify existing code and design patterns in the file/module.
3. **Planning**: Present a short, objective implementation plan to the user.
4. **Authorization**: Wait for user authorization before making significant structural changes.
5. **Execution**: Strictly implement the requested step.
6. **Review**: Review the changes and report the modified files.

---

# Testing and Quality

- Every new business rule must have an automated test when applicable.
- Prefer simple, focused tests (Unit tests with `pytest` on the backend).
- Do not remove or weaken existing tests to make the implementation pass.
- Before completing a step, run the configured test suite:
  - Backend API: `pytest` in `backend/api/`
  - Backend ML: `pytest` in `backend/ml/`
  - Frontend: `npm test` or `npm run build` in `frontend/`

---

# Git and Commits

- Do not run Git commands that create or send commits (`git commit`, `git push`) unless explicitly requested by the user.

---

# Agent Autonomy Limits

### The Agent CAN:

- Read files and analyze the Melitrack codebase;
- Modify files directly related to the current task;
- Create and update automated tests;
- Run local verification, testing, and build commands (e.g., `pytest`, `npm run dev`, `kubectl apply --dry-run`);
- Offer technical and architectural suggestions.

### The Agent CANNOT (without explicit authorization):

- Push to the remote repository;
- Create or send Git commits;
- Delete database migrations (`alembic/versions`);
- Add new dependencies (`pip install`, `npm install`) without proven necessity;
- Perform large structural refactorings across multiple modules simultaneously;
- Run commands that destroy volumes or break the Docker/Kubernetes environment.

---

# Completion of Each Task

Upon finishing an instruction, the agent must mandatorily report:

1. **What was implemented**.
2. **Which files were created or modified** (with links in the format `file:///path`).
3. **What technical decisions were made** (if any).
4. **If there are any pending issues**.

After that, stop immediately and await new instructions from the user.
