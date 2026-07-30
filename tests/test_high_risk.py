import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.reasoning_agent import analyze

from agents.reasoning_agent import analyze

metrics = {
    "cpu": 95,
    "memory": 90,
    "network": 150,
    "network_out": 120,
    "status_check": 1,
    "instance_state": "running"
}

result = analyze(metrics)
print(result)