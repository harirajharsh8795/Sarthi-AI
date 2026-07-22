# Saarthi AI - DevOps Architecture & Operations Handbook

This document outlines the DevOps architecture, container strategy, security controls, and resource monitoring framework for **Saarthi AI**.

---

## 1. System Architecture Diagram

```
+-----------------------------------------------------------------------+
|                           Nginx Reverse Proxy                         |
|                               (Port 80)                               |
+-----------------------------------++----------------------------------+
                                    ||
                +-------------------v------------------+
                |          FastAPI Backend Container   |
                |               (Port 8000)            |
                +-------------------+------------------+
                                    |
        +---------------------------+--------------------------+
        |                           |                          |
+-------v-------+           +-------v-------+          +-------v-------+
|  ChromaDB     |           |   SQLite DB   |          |  Ollama LLM   |
| Vector Engine |           | Relational Store|        | Service (11434)|
+---------------+           +---------------+          +---------------+
```

---

## 2. Resource & Health Monitoring

The background module `backend/resource_monitor.py` tracks:
- **CPU & RAM**: Live percent utilization and memory thresholds.
- **GPU (Jetson NVML)**: GPU core & memory usage for edge inference.
- **Ollama**: Service connectivity and model readiness (`llama3.2:1b`).
- **ChromaDB**: Document & chunk count in collection `saarthi_kb`.

---

## 3. Zero-Downtime Deployment Strategy

1. Pre-deployment backup generated via `scripts/backup_db.py`.
2. Database schema updated automatically via `scripts/migrate_db.py`.
3. New container spun up in parallel; Nginx re-routes traffic after container passes `backend/health_check.py`.
4. Automatic rollback executed via `scripts/rollback_db.py` on health check failure.
