def analyze(metrics):

    cpu = metrics["cpu"]

    memory = metrics["memory"]

    network_in = metrics["network"]

    network_out = metrics["network_out"]

    status_check = metrics["status_check"]

    instance_state = metrics["instance_state"]


    # EC2 not running
    if instance_state != "running":

        return {
            "scenario": "INSTANCE_OFFLINE",
            "severity": "HIGH",
            "reason": f"EC2 instance is currently {instance_state}.",
            "confidence": 99
        }


    # AWS health issue
    if status_check > 0:

        return {
            "scenario": "STATUS_CHECK_FAILED",
            "severity": "HIGH",
            "reason": "AWS reported a failed EC2 status check.",
            "confidence": 98
        }


    # High CPU with high incoming traffic
    if cpu > 80 and network_in > 100:

        confidence = min(99, 90 + int((cpu - 80) / 2))

        return {
            "scenario": "HIGH_CPU",
            "severity": "HIGH",
            "reason": "High CPU utilization with increased network traffic.",
            "confidence": confidence
        }


    # High outgoing traffic
    if network_out > 100:

        return {
            "scenario": "NETWORK_SPIKE",
            "severity": "MEDIUM",
            "reason": "High outgoing network traffic detected.",
            "confidence": 92
        }


    # Memory (currently simulated)
    if memory > 85:

        confidence = min(99, 90 + int((memory - 85) / 2))

        return {
            "scenario": "HIGH_MEMORY",
            "severity": "HIGH",
            "reason": "Memory utilization is critically high.",
            "confidence": confidence
        }


    return {
        "scenario": "HEALTHY",
        "severity": "LOW",
        "reason": "Infrastructure is operating normally.",
        "confidence": 99
    }