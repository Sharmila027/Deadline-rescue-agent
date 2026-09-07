import re

from app.agent.priority import prioritize_tasks
from app.agent.planner import create_plan
from app.agent.reasoner import reason_about_change


def apply_task_order(tasks, task_order):

    task_map = {
        task["name"].lower(): task
        for task in tasks
    }

    ordered = []
    added = set()

    for name in task_order:

        name = name.lower()

        if name in task_map and name not in added:

            ordered.append(task_map[name])
            added.add(name)

    for task in tasks:

        name = task["name"].lower()

        if name not in added:

            ordered.append(task)
            added.add(name)

    return ordered


def get_extra_time(reason):

    text = reason.lower()

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(hour|hours|hr|hrs)",
        text
    )

    if match:
        return float(match.group(1))

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(minute|minutes|min|mins)",
        text
    )

    if match:
        return float(match.group(1)) / 60

    return 0


def replan(tasks, reason, changed_task=None):

    print("\n[REPLANNING]")
    print("Reason:", reason)

    if changed_task:

        for task in tasks:

            if task["name"].lower() == changed_task.lower():

                print(
                    "[AGENT] Change detected for:",
                    task["name"]
                )

                extra_time = get_extra_time(reason)

                if extra_time > 0:

                    task["duration"] += extra_time

                    print(
                        "[AGENT] Added extra time:",
                        extra_time,
                        "hours"
                    )

                print(
                    "[AGENT] New duration:",
                    task["duration"],
                    "hours"
                )

    prioritized = prioritize_tasks(tasks)

    print(
        "\n[AGENT] Asking AI to re-evaluate the schedule..."
    )

    decision = reason_about_change(
        prioritized,
        reason,
        changed_task
    )

    print("\n[AI REPLANNING DECISION]")
    print("Action:", decision["action"])
    print("Reason:", decision["reason"])

    print("\n[AGENT] New AI-selected order:")

    for i, task_name in enumerate(
        decision["task_order"],
        1
    ):
        print(i, "-", task_name)

    ordered_tasks = apply_task_order(
        prioritized,
        decision["task_order"]
    )

    new_plan = create_plan(ordered_tasks)

    return new_plan, decision