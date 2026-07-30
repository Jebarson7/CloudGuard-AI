from openrouter_ai import predictive_failure_ai

def predict_failure(metrics):
    """
    Predictive Failure AI Agent

    Input:
        Cloud metrics from AWS

    Output:
        AI prediction about system health and possible failures.
    """

    cpu = metrics["cpu"]
    memory = metrics["memory"]
    network = metrics["network"]
    status_check = metrics["status_check"]

    prediction = predictive_failure_ai(
        cpu,
        memory,
        network,
        status_check
    )

    return prediction