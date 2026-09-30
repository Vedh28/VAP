import json
import subprocess
import ollama
import psutil

MODEL_NAME = "qwen/qwen3.8-27b"
def get_system_merics()->str:
    """Returns local host system resource utilization (CPU,RAM, DISK) as a JSON string."""
    metrics={
        "cpu":psutil.cpu_percent(interval=1),
        "memory":psutil.virtual_memory().percent,
        "disk":psutil.disk_usage('/').percent
    }
    return json.dumps(metrics)
def ping_hostsa(hostname:str)->str:
    """Pings a hostname and returns the result as a JSON string.
    Args:
        hostname (str): Domain name or IP address to ping (e.g. '1.1.1.1' or 'google.com').
        """
    try:
        res = subprocess.check_output(["ping", "-c", "4", hostname], stderr=subprocess.STDOUT, universal_newlines=True)
        return json.dumps({"status": "success", "raw_output": res.strip()})
     except subprocess.CalledProcessError as e:
        return json.dumps({"status": "error", "error_message": str(e)})
    except Exception as err:
        return json.dumps({"status": "error", "error_message": str(err)})

#Map function names to executable python functions
SYSTEM_TOOLS = {"get_system_metrics": get_system_metrics}
NETWORK_TOOLS_MAP = {"ping_hosts": ping_hosts}