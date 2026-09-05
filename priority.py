from app.tools.time_tool import hours_until


def calculate_priority(task):
    hours = hours_until(task["deadline"])

    urgency = max(0, 100 - hours * 4)

    score = urgency + task["importance"] * 10

    if task["completed"]:
        score = 0

    return round(score, 2)


def prioritize_tasks(tasks):
    for task in tasks:
        task["priority"] = calculate_priority(task)

    return sorted(
        tasks,
        key=lambda x: x["priority"],
        reverse=True
    )