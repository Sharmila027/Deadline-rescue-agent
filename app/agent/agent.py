from app.tools.task_tool import get_tasks
from app.agent.priority import prioritize_tasks
from app.agent.planner import create_plan
from app.agent.replanner import replan
from app.agent.reasoner import reason_about_tasks
from app.agent.monitor import monitor_tasks
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

        print(
            "[AGENT] Asking AI to decide task order..."
        )

        decision = reason_about_tasks(prioritized)

        print("\n[AI DECISION]")
        print("Action:", decision["action"])
        print("Reason:", decision["reason"])

        ordered_tasks = self.apply_task_order(
            prioritized,
            decision["task_order"]
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

        new_plan, decision = replan(
            tasks,
            reason,
            changed_task
        )

        print("\n[AGENT] Executing new plan...")

        self.execute_plan(new_plan)

        self.memory.remember({
            "event": "replanned",
            "reason": reason,
            "changed_task": changed_task,
            "decision": decision,
            "plan": new_plan
        })

        send_notification(
            "Your schedule changed. A new plan has been created."
        )

        return new_plan

    def monitor(self):

        print("\n[AGENT] Monitoring schedule...")

        tasks = get_tasks()

        alerts = monitor_tasks(tasks)

        if not alerts:

            print("[AGENT] Schedule is safe.")

            self.memory.remember({
                "event": "monitor",
                "status": "safe"
            })

            return {
                "alerts": [],
                "replanned": False,
                "plan": []
            }

        print("\n[AGENT] Problems detected!")

        for alert in alerts:

            print(
                "[ALERT]",
                alert["task"],
                "-",
                alert["reason"]
            )

        first_alert = alerts[0]

        print(
            "\n[AGENT] Automatically triggering replanning..."
        )

        new_plan = self.handle_change(
            first_alert["reason"],
            first_alert["task"]
        )

        self.memory.remember({
            "event": "automatic_replan",
            "alerts": alerts
        })

        return {
            "alerts": alerts,
            "replanned": True,
            "plan": new_plan
        }