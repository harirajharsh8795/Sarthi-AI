# Saarthi AI - Database Backup & Automated Recovery Handbook

This document describes the automated database backup, migration, and disaster recovery procedures for **Saarthi AI**.

---

## 1. Automated Pre-Deployment Backup

Before any deployment, the CI/CD pipeline automatically executes `scripts/backup_db.py`, creating a timestamped backup directory in `backups/backup_YYYYMMDD_HHMMSS/` containing:
- `saarthi.db` (SQLite Database)
- `chroma_db/` (Vector Store)
- `bm25_index.pkl` (Sparse Index)
- `knowledge_graph.json` (Knowledge Graph)

---

## 2. Automated Rollback Trigger

If post-deployment health checks (`backend/health_check.py`) fail, the pipeline immediately triggers `scripts/rollback_db.py`.

```bash
# Manual Rollback Trigger (if needed)
python scripts/rollback_db.py
```

---

## 3. Database Migration Procedures

Migrations are managed non-destructively via `scripts/migrate_db.py`.
