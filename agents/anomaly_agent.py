def detect_anomaly(metrics):

    cpu = metrics["cpu"]
    memory = metrics["memory"]
    network_in = metrics["network"]
    network_out = metrics["network_out"]
    status_check = metrics["status_check"]
    instance_state = metrics["instance_state"]

    # 1. EC2 Instance State
    if instance_state != "running":

        return {
            "status": "anomaly",
            "title": "🔴 EC2 Instance Offline",
            "message": f"The EC2 instance is currently {instance_state}."
        }

    # 2. AWS Status Check
    if status_check > 0:

        return {
            "status": "anomaly",
            "title": "⚠️ AWS Status Check Failed",
            "message": "CloudWatch detected an EC2 status check failure."
        }

    # 3. High CPU + High Network
    if cpu > 80 and network_in > 100:

        return {
            "status": "anomaly",
            "title": "⚠️ High CPU Spike",
            "message": "High CPU utilization and increased incoming network traffic detected."
        }

    # 4. High Outgoing Network
    elif network_out > 100:

        return {
            "status": "anomaly",
            "title": "⚠️ High Network Traffic",
            "message": "Abnormally high outgoing network traffic detected."
        }

    # 5. High Memory (currently simulated)
    elif memory > 85:

        return {
            "status": "anomaly",
            "title": "⚠️ Memory Pressure",
            "message": "Potential memory leak or high memory utilization detected."
        }

    # 6. Everything Healthy
    return {
        "status": "normal",
        "title": "✅ Infrastructure Healthy",
        "message": "All monitored AWS metrics are within normal operating ranges."
    }