import re
from utils.openrouter_ai import ask_ai

def generate_plan(metrics, scenario):

    cpu = metrics["cpu"]

    memory = metrics["memory"]

    network = metrics["network"]

    network_out = metrics["network_out"]

    status_check = metrics["status_check"]

    instance_state = metrics["instance_state"]

    risk = metrics["risk"]

    prompt = f"""
    You are CloudGuard AI Planning Agent.

    Scenario: {scenario}

    Current AWS Metrics

    CPU Usage: {cpu}%

    Memory Usage: {memory}%

    Network In: {network} KB

    Network Out: {network_out} KB

    Status Check Failed: {status_check}

    EC2 Instance State: {instance_state}

    Risk Level: {risk}

    Decision Rules:

    If EC2 Instance State is not "running":
    - Recommend checking why the instance is offline.
    - Recommend starting the EC2 instance if appropriate.
    - Do not recommend Auto Scaling.

    If Status Check Failed is greater than 0:
    - Recommend checking EC2 system status.
    - Recommend reviewing CloudWatch metrics.
    - Investigate AWS infrastructure health before rebooting.

    If Scenario is HEALTHY:
    - Recommend ONLY monitoring.
    - Recommend periodic health checks.
    - Do NOT recommend restarting EC2.
    - Do NOT recommend Auto Scaling.
    - Do NOT recommend notifying engineers.

    If Scenario is HIGH_CPU:
    - Review CloudWatch metrics.
    - Review application logs.
    - Verify Auto Scaling.

    If Scenario is HIGH_MEMORY:
    - Check memory usage.
    - Investigate memory leaks.
    - Monitor processes.

    If Scenario is NETWORK_SPIKE:
    - Review network traffic.
    - Check Load Balancer.
    - Inspect AWS WAF logs.

    Return ONLY three numbered actions.

    Maximum 6 words each.

    Example:

    1. Monitor CloudWatch metrics
    2. Perform health checks
    3. No remediation required
    """

    response = ask_ai(
        prompt,
        cpu,
        memory,
        network,
        risk
    )

    steps = []

    for line in response.splitlines():

        line = line.strip()

        if re.match(r"^\d+\.", line):
            steps.append(line)

    return steps