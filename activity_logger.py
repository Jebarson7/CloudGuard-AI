from datetime import datetime
import json
import os

LOG_FILE = "activity_log.json"


def log_activity(action, status):

    log = {
        "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "action": action,
        "status": status
    }

    if os.path.exists(LOG_FILE):

        with open(LOG_FILE, "r") as file:
            logs = json.load(file)

    else:

        logs = []

    logs.append(log)

    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)


def get_logs():

    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r") as file:
        return json.load(file)