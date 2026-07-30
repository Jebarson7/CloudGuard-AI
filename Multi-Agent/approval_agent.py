def request_approval(risk):

    if risk == "HIGH RISK":
        return {
            "required": True,
            "message": "High-risk action detected. Human approval is required."
        }

    elif risk == "MEDIUM RISK":
        return {
            "required": True,
            "message": "Medium-risk action. Approval is recommended."
        }

    return {
        "required": False,
        "message": "Low-risk action. No approval required."
    }