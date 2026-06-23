def cost_advice(cpu, memory):

    if cpu < 10:
        return """
💰 Cost Optimization Recommendation

• EC2 utilization is very low.
• Consider downgrading to a smaller instance.
• Potential cost savings: 20% - 40%.
• Risk Level: Low.
"""

    elif cpu < 40:
        return """
💰 Cost Optimization Recommendation

• Current utilization is moderate.
• No immediate scaling changes required.
• Monitor workload trends.
"""

    else:
        return """
💰 Cost Optimization Recommendation

• Instance utilization is healthy.
• Keep current instance size.
• Consider Auto Scaling for peak traffic.
"""