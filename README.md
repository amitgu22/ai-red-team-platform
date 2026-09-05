# AI Red Team Platform — Phase 1

A Dockerized proof-of-concept for a vendor-neutral AI red-teaming platform.

## Phase 1 includes

- React + Vite frontend
- FastAPI backend
- PostgreSQL
- Redis
- Sample AI target application
- Provider/plugin abstraction for Promptfoo, PyRIT, Garak and Striker
- Dashboard
- Provider onboarding
- Target management
- Docker Compose local environment

> This repository is a security-testing POC. Use only against systems and models you are authorized to test.

## Quick start

```bash
docker compose up --build
```

Open:

- Frontend: http://localhost:3000
- API: http://localhost:8000
- API docs: http://localhost:8000/docs
- Sample target: http://localhost:9000

## GitHub

```bash
git init
git add .
git commit -m "Initial Phase 1 AI red team platform"
git branch -M main
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

## Architecture

```text
React UI
   |
FastAPI API
   |
   +-- PostgreSQL
   +-- Redis
   +-- Provider Registry
   |     +-- Promptfoo
   |     +-- PyRIT
   |     +-- Garak
   |     +-- Striker
   |
   +-- Sample Target
```

## Roadmap

Phase 2: scenarios, strategies, campaign orchestration and execution workers.

Phase 3: normalized results, evaluators, findings, evidence and recommendations.

Phase 4: reporting, attack-surface analytics and AWS deployment.
