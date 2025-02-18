import os
import psutil
import socket
import platform
import logging
from datetime import datetime

logger = logging.getLogger('p2p_agent')

def collect_system_specs(device_id=None):
    """Collect static system specifications"""
    # Use the correct root path for Windows systems (cross-platform)
    root_dir = os.path.abspath(os.sep)  # This should now work on both Windows and other OSes

    specs = {
        "device_id": device_id,
        "platform": platform.system(),
        "platform_version": platform.version(),
        "processor": platform.processor(),
        "hostname": socket.gethostname(),
        "cpu_count_physical": psutil.cpu_count(logical=False),
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "total_memory": psutil.virtual_memory().total,
        "total_disk": psutil.disk_usage(root_dir).total  # Corrected to use the root dir dynamically
    }

    # Check for GPU
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            specs["gpu_count"] = len(gpus)
            specs["gpu_names"] = [gpu.name for gpu in gpus]
            specs["gpu_memory"] = [gpu.memoryTotal for gpu in gpus]
    except ImportError:
        specs["gpu_count"] = 0

    return specs

def collect_metrics():
    """Collect system metrics like CPU, memory, and disk usage"""
    metrics = {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent  # You can change this if you want specific partition usage
    }
    return metrics
