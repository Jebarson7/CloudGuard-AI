def execute_action(scenario, approval):

    if approval["required"]:

        return {
            "executed": False,
            "status": "Waiting for Human Approval",
            "action": "No action executed."
        }

    actions = {

        "HEALTHY": "Monitor",

        "HIGH_CPU": "Reboot EC2",

        "HIGH_MEMORY": "Reboot EC2",

        "NETWORK_SPIKE": "Create CloudWatch Alarm"

    }

    return {
        "executed": True,
        "status": "Completed",
        "action": actions.get(
            scenario,
            "Monitoring only."
        )
    }