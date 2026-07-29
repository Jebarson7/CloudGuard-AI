from datetime import datetime

def generate_report(metrics, action):

    report = f"""
CloudGuard AI Infrastructure Report

Generated:
{datetime.now()}

----------------------------------

CPU Usage:
{metrics['cpu']}%

Memory Usage:
{metrics['memory']}%

Network:
{metrics['network']} KB

Risk:
{metrics['risk']}

Last Action:
{action['action']}

Status:
{action['status']}
"""

    return report