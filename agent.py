from app.tools.task_tool import get_tasks
from app.agent.priority import prioritize_tasks
from app.agent.planner import create_plan
from app.agent.replanner import replan
from app.agent.reasoner import reason_about_tasks
from app.tools.notification_tool import send_notification
from app.tools.calendar_tool import add_event


class DeadlineRescueAgent:

    def __init__(self, memory):
        self.memory = memory

    def analyze(self):

        print("\n[AGENT] Observing tasks...")

        tasks = get_tasks()

        if not tasks:
            print("[AGENT] No tasks found.")
            return []

        print("[AGENT] Calculating priorities...")

        prioritized = prioritize_tasks(tasks)

        print("[AGENT] Asking AI to decide task order...")

        decision = reason_about_tasks(prioritized)

        print("\n[AI DECISION]")
        print("Action:", decision["action"])
        print("Reason:", decision["reason"])

        task_order = decision["task_order"]

        print("\n[AGENT] AI selected order:")

        for i, task_name in enumerate(task_order, 1):
            print(i, "-", task_name)

        ordered_tasks = self.apply_task_order(
            prioritized,
            task_order
        )

        print("\n[AGENT] Creating schedule...")

        plan = create_plan(ordered_tasks)

        self.execute_plan(plan)

        self.memory.remember({
            "event": "plan_created",
            "decision": decision,
            "plan": plan
        })

        return plan

    def apply_task_order(self, tasks, task_order):

        task_map = {
            task["name"].lower(): task
            for task in tasks
        }

        ordered = []

        for name in task_order:

            task = task_map.get(name.lower())

            if task:
                ordered.append(task)

        for task in tasks:

            if task not in ordered:
                ordered.append(task)

        return ordered

    def execute_plan(self, plan):

        print("\n[AGENT] Executing plan...")

        for item in plan:

            add_event(
                item["task"],
                item["start"],
                item["end"]
            )

    def handle_change(self, reason, changed_task):

        print("\n[AGENT] Change detected!")
        print("[AGENT] Reason:", reason)

        tasks = get_tasks()

        print("[AGENT] Re-evaluating tasks...")

        new_plan = replan(
            tasks,
            reason,
            changed_task
        )

        print("[AGENT] Executing new plan...")

        self.execute_plan(new_plan)

        self.memory.remember({
            "event": "replanned",
            "reason": reason,
            "changed_task": changed_task,
            "plan": new_plan
        })

        send_notification(
            "Your schedule changed. A new plan has been created."
        )

        return new_plan