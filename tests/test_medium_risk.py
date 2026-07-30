import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.reasoning_agent import analyze

metrics = {
    "cpu": 20,
    "memory": 60,
    "network": 20,
    "network_out": 150,
    "status_check": 0,
    "instance_state": "running"
}

result = analyze(metrics)
print(result)