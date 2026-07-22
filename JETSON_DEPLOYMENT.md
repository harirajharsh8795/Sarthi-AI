# Saarthi AI - Jetson Orin Edge Deployment Guide

This guide describes how to deploy **Saarthi AI** on NVIDIA Jetson Orin Nano / AGX Orin edge hardware following EdgeMinds guidelines.

---

## 1. Hardware Requirements & Optimization Rules

- **Target Device**: NVIDIA Jetson Orin Nano / AGX Orin (JetPack 5.1+ / 6.0)
- **Model**: `llama3.2:1b` running on local Ollama service.
- **Ollama Directive**: Do **NOT** reinstall or overwrite existing Ollama service. Use existing systemd `ollama` daemon.

---

## 2. Environment Setup

```bash
# Export Ollama Host for local container communication
export OLLAMA_HOST=http://localhost:11434
export MODEL_NAME=llama3.2:1b

# Memory Optimization flags for Jetson ARM64
export OMP_NUM_THREADS=4
export MALLOC_TRIM_THRESHOLD_=100000

# Test Ollama Service Connectivity
curl http://localhost:11434/api/tags
```

---

## 3. Container Deployment on Jetson

```bash
docker-compose -f docker-compose.prod.yml up -d
```
