from datetime import datetime, timedelta


def create_plan(tasks):

    current_time = datetime.now()

    plan = []

    for task in tasks:

        if task["completed"]:
            continue

        start_time = current_time

        end_time = (
            current_time +
            timedelta(hours=task["duration"])
        )

        deadline = datetime.strptime(
            task["deadline"].strip(),
            "%Y-%m-%d %H:%M"
        )

        status = "On Time"

        if end_time > deadline:
            status = "At Risk"

        plan.append({
            "task": task["name"],
            "priority": task["priority"],
            "start": start_time.strftime(
                "%Y-%m-%d %H:%M"
            ),
            "end": end_time.strftime(
                "%Y-%m-%d %H:%M"
            ),
            "deadline": task["deadline"],
            "status": status
        })

        current_time = end_time

    return plan