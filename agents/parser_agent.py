def extract_root_cause(scenario):

    mapping = {
        "HEALTHY": "Healthy Infrastructure",
        "HIGH_CPU": "High CPU Utilization",
        "HIGH_MEMORY": "Memory Pressure",
        "NETWORK_SPIKE": "Network Traffic Spike"
    }

    return mapping.get(scenario, "Unknown") 