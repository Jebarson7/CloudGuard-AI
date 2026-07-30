def cost_advice(cpu, memory, cost):

    if cost == 0:

        return f"""
💰 AWS Cost Optimization

Current Monthly Cost: ${cost:.2f}

• Your AWS usage is currently within the Free Tier or has no billable charges.
• No immediate cost optimization is required.
• Continue monitoring your AWS resources.
"""

    elif cpu < 10:

        return f"""
💰 AWS Cost Optimization

Current Monthly Cost: ${cost:.2f}

• EC2 utilization is very low.
• Consider stopping idle EC2 instances.
• Consider using a smaller EC2 instance.
• Potential cost savings: 20% - 40%.
"""

    elif cpu < 40:

        return f"""
💰 AWS Cost Optimization

Current Monthly Cost: ${cost:.2f}

• Current utilization is moderate.
• No immediate scaling changes are required.
• Continue monitoring monthly AWS costs.
"""

    else:

        return f"""
💰 AWS Cost Optimization

Current Monthly Cost: ${cost:.2f}

• Instance utilization is healthy.
• Keep the current instance size.
• Consider Auto Scaling for peak workloads.
"""