from datetime import datetime


def monitor_tasks(tasks):

    alerts = []

    for task in tasks:

        if task["completed"]:
            continue

        deadline = datetime.strptime(
            task["deadline"].strip(),
            "%Y-%m-%d %H:%M"
        )

        now = datetime.now()

        available_hours = (
            deadline - now
        ).total_seconds() / 3600

        required_hours = task["duration"]

        print(
            "[MONITOR]",
            task["name"],
            "| Available:",
            round(available_hours, 2),
            "hours | Required:",
            required_hours,
            "hours"
        )

        if available_hours < required_hours:

            alerts.append({
                "task": task["name"],
                "reason": "Not enough time before deadline"
            })

    return alerts