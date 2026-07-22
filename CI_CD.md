# Saarthi AI - GitHub Actions CI/CD Pipeline Manual

This document details the complete CI/CD automation workflow configured in `.github/workflows/`.

---

## 1. Workflow Summary

| Workflow File | Trigger | Responsibility |
| :--- | :--- | :--- |
| `security.yml` | Push / PR | Bandit code security, Safety dependency check, Secret scanning |
| `backend.yml` | Push / PR | Black, Flake8, Pytest test suite |
| `frontend.yml` | Push / PR | Vite/React linting and production build |
| `rag-ingestion.yml` | `knowledge_base/**` changes | Markdown validation, incremental chunking, embeddings & BM25 update |
| `docker.yml` | Push to `main` | Production Docker image build & tag |
| `deploy.yml` | Successful Docker build | Timestampped backup, DB migration, zero-downtime deploy & health check |

---

## 2. Security & Compliance Controls

- **Bandit**: Static security analysis for Python code.
- **Safety**: Dependency vulnerability scanner.
- **Secret Scanner**: Custom pattern matcher detecting leaked API keys or credentials.
