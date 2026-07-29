import json
import os

FILE = "memory.json"

def load_memory():

    if not os.path.exists(FILE):
        return []

    with open(FILE, "r") as f:
        return json.load(f)


from datetime import datetime

def save_incident(
    cpu,
    memory,
    network,
    risk,
    scenario,
    root_cause,
    plan,
    action,
    status
):

    incidents = load_memory()

    incidents.append({

        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "cpu": cpu,

        "memory": memory,

        "network": network,

        "scenario": scenario,

        "risk": risk,

        "root_cause": root_cause,

        "plan": plan,

        "action": action,

        "status": status

    })

    with open(FILE, "w") as f:
        json.dump(incidents, f, indent=4)


def find_similar(scenario):

    incidents = load_memory()

    return [
        incident
        for incident in incidents
        if incident["scenario"] == scenario
    ]