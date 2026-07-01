import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Add parent directory to system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from edge_runtime import edge_runtime_optimizer
from resource_monitor import resource_monitor
from model_manager import model_lifecycle_manager
from offline_engine import offline_engine
from cache_manager import cache_manager
from benchmark_service import benchmark_service
from deployment_validator import deployment_validator
from diagnostics import system_diagnostics
from edge_score import edge_performance_scorecard

client = TestClient(app)

def test_performance_profiles():
    """Checks switching thread parameters for different profiles."""
    edge_runtime_optimizer.set_profile("Power Saver")
    assert edge_runtime_optimizer.profile_name == "Power Saver"
    assert edge_runtime_optimizer.max_workers == 1
    
    edge_runtime_optimizer.set_profile("Performance")
    assert edge_runtime_optimizer.profile_name == "Performance"
    assert edge_runtime_optimizer.max_workers >= 2

def test_memory_autotune():
    """Verifies that high-load checks trigger memory shrinkage actions."""
    # Simulate high RAM usage
    with patch("psutil.virtual_memory") as mock_mem:
        mock_mem.return_value.percent = 95.0
        mock_mem.return_value.available = 100 * 1024 * 1024
        
        # Trigger autotune
        res = edge_runtime_optimizer.auto_tune_runtime()
        assert "Shrinkage" in res["action_taken"]

def test_resource_monitor_timeline():
    """Verifies rolling history maintains length constraints."""
    history = resource_monitor.get_timeline_data()
    assert len(history) >= 1
    assert "cpu_pct" in history[0]
    assert "ram_pct" in history[0]

def test_offline_checklist():
    """Validates connectivity checkers and offline readiness values."""
    res = offline_engine.check_offline_readiness()
    assert "offline_score" in res
    assert "checklist" in res
    assert "internet_offline" in res["checklist"]

def test_lru_cache_operations():
    """Verifies standard LRU set/get evictions and hits."""
    cache_manager.clear_all()
    cache_manager.ocr_cache.set("key1", "val1")
    assert cache_manager.ocr_cache.get("key1") == "val1"
    assert cache_manager.ocr_cache.get("key2") is None
    
    # Eviction check
    cap = cache_manager.ocr_cache.capacity
    for i in range(cap + 10):
        cache_manager.ocr_cache.set(f"k_{i}", f"v_{i}")
    # key1 should have been evicted
    assert cache_manager.ocr_cache.get("key1") is None

def test_system_diagnostics():
    """Validates self-diagnostics checks return healthy recommendations."""
    res = system_diagnostics.diagnose_system()
    assert "overall_health" in res
    assert "recommended_actions" in res

def test_edge_scorecard():
    """Checks compilation weights of the Edge Readiness Score."""
    res = edge_performance_scorecard.calculate_readiness_score()
    assert "edge_readiness_score" in res
    assert "readiness_label" in res

def test_endpoints_dashboards():
    """Checks REST dashboard APIs return status_code 200."""
    response = client.get("/api/v1/system/health")
    assert response.status_code == 200
    
    response = client.get("/api/v1/system/resources")
    assert response.status_code == 200
    data = response.json()
    assert "current_snapshot" in data
    
    response = client.get("/api/v1/system/cache")
    assert response.status_code == 200
