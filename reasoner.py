import os
import json
from openai import OpenAI


def reason_about_tasks(tasks):

    if not tasks:
        return {
            "action": "WAIT",
            "task_order": [],
            "reason": "No tasks available."
        }

    if not os.environ.get("OPENAI_API_KEY"):
        return {
            "action": "WAIT",
            "task_order": [],
            "reason": "API key is not available."
        }

    client = OpenAI()

    task_text = ""

    for task in tasks:
        task_text += f"""
Task: {task['name']}
Deadline: {task['deadline']}
Duration: {task['duration']} hours
Importance: {task['importance']}/5
Priority: {task.get('priority', 0)}
Completed: {task['completed']}
"""

    prompt = f"""
You are the decision-making engine of a Deadline Rescue Agent.

Analyze the tasks below and decide the best order.

{task_text}

Return ONLY valid JSON in this format:

{{
    "action": "PLAN",
    "task_order": ["task name 1", "task name 2", "task name 3"],
    "reason": "short explanation"
}}

Rules:
- Put the most urgent and important task first.
- Consider deadline, duration, importance and priority.
- Do not invent tasks.
- Use the exact task names provided.
"""

    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        result = json.loads(response.output_text)

        return result

    except Exception as e:
        return {
            "action": "WAIT",
            "task_order": [],
            "reason": f"AI reasoning failed: {e}"
        }