from app.agent.priority import prioritize_tasks
from app.agent.planner import create_plan


def replan(tasks, reason, changed_task=None):

    print("\n[REPLANNING]")
    print("Reason:", reason)

    if changed_task:
        for task in tasks:
            if task["name"].lower() == changed_task.lower():
                task["importance"] = 10
                task["duration"] += 1

                print("[AGENT] Updated task:", task["name"])
                print("[AGENT] New duration:", task["duration"], "hours")

    prioritized = prioritize_tasks(tasks)

    new_plan = create_plan(prioritized)

    return new_plan