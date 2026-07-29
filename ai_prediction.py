def predict_risk(cpu, memory, network):

    score = 0

    if cpu > 80:
        score += 40
    elif cpu > 50:
        score += 20

    if memory > 80:
        score += 40
    elif memory > 50:
        score += 20

    if network > 500:
        score += 20

    if score >= 70:
        return "HIGH RISK"
    elif score >= 40:
        return "MEDIUM RISK"
    else:
        return "LOW RISK"

def predict_failure(cpu, memory, network, alarm_state):

    if alarm_state == "ALARM":
        return {
            "status": "Critical",
            "failure": "Service Failure",
            "probability": "95%"
        }

    elif cpu > 90:
        return {
            "status": "High",
            "failure": "CPU Overload",
            "probability": "90%"
        }

    elif memory > 90:
        return {
            "status": "High",
            "failure": "Memory Exhaustion",
            "probability": "90%"
        }

    elif network > 500:
        return {
            "status": "Medium",
            "failure": "Network Congestion",
            "probability": "70%"
        }

    else:
        return {
            "status": "Low",
            "failure": "No Immediate Failure Expected",
            "probability": "10%"
        }