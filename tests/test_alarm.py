from aws_cloudwatch import get_alarm_status

alarms = get_alarm_status()

if alarms:

    for alarm in alarms:

        print("Alarm Name :", alarm["name"])
        print("State      :", alarm["state"])
        print("Reason     :", alarm["reason"])
        print("Updated    :", alarm["updated"])
        print("-" * 40)

else:

    print("No alarms found.")