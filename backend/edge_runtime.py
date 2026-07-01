import os
import sys
import platform
import psutil
import logging
import shutil
import gc
from config import settings

logger = logging.getLogger("saarthi.edge")

class EdgeRuntimeOptimizer:
    """
    Optimizes system threads, worker execution pools, and caching bounds
    based on hardware profile detection (Jetson, ARM64, x86).
    """
    
    def __init__(self):
        self.profile_name = "Balanced"
        self.max_workers = 2
        self.cache_capacity = 200
        self.low_power_mode = False
        self.detect_and_initialize()

    def is_nvidia_jetson(self) -> bool:
        """Heuristically detects if running on NVIDIA Jetson."""
        # 1. Check L4T folder path
        if os.path.exists("/etc/nv_tegra_release") or os.path.exists("/usr/lib/nvidia"):
            return True
        # 2. Check CPU model
        try:
            with open("/proc/cpuinfo", "r") as f:
                content = f.read().lower()
                if "nvidia" in content or "tegra" in content:
                    return True
        except Exception:
            pass
        return False

    def detect_and_initialize(self):
        """Initializes system profile based on architecture and memory bounds."""
        self.arch = platform.machine()
        self.cores = psutil.cpu_count(logical=True) or 2
        
        mem = psutil.virtual_memory()
        self.total_ram_gb = mem.total / (1024 ** 3)
        
        self.jetson_detected = self.is_nvidia_jetson()
        
        # Determine defaults based on hardware limitations
        if self.jetson_detected or self.total_ram_gb < 6.0 or self.cores <= 2:
            self.set_profile("Power Saver")
        else:
            self.set_profile("Balanced")

    def set_profile(self, name: str):
        """Sets active profile parameters."""
        valid_profiles = {"Power Saver", "Balanced", "Performance", "Demo"}
        if name not in valid_profiles:
            name = "Balanced"
            
        self.profile_name = name
        
        if name == "Power Saver":
            self.max_workers = 1
            self.cache_capacity = 50
            self.low_power_mode = True
        elif name == "Balanced":
            self.max_workers = min(2, self.cores)
            self.cache_capacity = 200
            self.low_power_mode = False
        elif name == "Performance":
            self.max_workers = min(4, self.cores)
            self.cache_capacity = 500
            self.low_power_mode = False
        elif name == "Demo":
            self.max_workers = min(6, self.cores)
            self.cache_capacity = 1000
            self.low_power_mode = False
            
        logger.info(f"Edge performance profile set to: {name} (Workers: {self.max_workers}, Cache: {self.cache_capacity})")

    def get_runtime_profile(self) -> dict:
        """Returns the hardware and execution settings metrics."""
        disk = shutil.disk_usage("/")
        mem = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            "profile_name": self.profile_name,
            "architecture": self.arch,
            "cpu_cores": self.cores,
            "total_ram_gb": round(self.total_ram_gb, 2),
            "free_ram_gb": round(mem.available / (1024 ** 3), 2),
            "swap_total_gb": round(swap.total / (1024 ** 3), 2),
            "swap_free_gb": round(swap.free / (1024 ** 3), 2),
            "disk_free_gb": round(disk.free / (1024 ** 3), 2),
            "jetson_detected": self.jetson_detected,
            "max_workers": self.max_workers,
            "cache_capacity": self.cache_capacity,
            "low_power_mode": self.low_power_mode
        }

    def auto_tune_runtime(self) -> dict:
        """
        Monitors active memory and CPU. If limits are crossed, triggers cache evictions
        and runs Garbage Collection.
        """
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percent()
        
        tuning_action = "None"
        
        if mem.percent > 85.0 or cpu > 90.0:
            tuning_action = "Triggered Memory Shrinkage"
            logger.warning(f"High load detected (RAM: {mem.percent}%, CPU: {cpu}%). Autotuner initiating GC...")
            
            # 1. Force release memory caches
            from cache_manager import cache_manager
            cache_manager.shrink_all_caches()
            
            # 2. Invoke GC
            gc.collect()
            
            # 3. If very critical, drop worker count down to 1
            if mem.percent > 92.0 and self.max_workers > 1:
                self.max_workers = 1
                tuning_action += " & Reduced Max Workers to 1"
                
        return {
            "cpu_usage_pct": cpu,
            "ram_usage_pct": mem.percent,
            "action_taken": tuning_action,
            "active_workers": self.max_workers
        }

edge_runtime_optimizer = EdgeRuntimeOptimizer()
