def generate_advice(cpu, memory, network):

    if cpu > 80:
        return "High CPU usage detected. Consider scaling resources."

    elif memory > 80:
        return "Memory usage is high. Check running services."

    else:
        return "System is operating normally."