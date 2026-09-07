import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


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
    "task_order": ["task name 1", "task name 2"],
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

        return json.loads(response.output_text)

    except Exception as e:

        return {
            "action": "WAIT",
            "task_order": [],
            "reason": f"AI reasoning failed: {e}"
        }


def reason_about_change(tasks, reason, changed_task):

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
You are the replanning engine of a Deadline Rescue Agent.

The user's schedule has changed.

CHANGE:
{reason}

CHANGED TASK:
{changed_task}

CURRENT TASKS:
{task_text}

Re-evaluate the situation and decide the best new task order.

Return ONLY valid JSON:

{{
    "action": "REPLAN",
    "task_order": ["task name 1", "task name 2"],
    "reason": "short explanation"
}}

Rules:
- Consider the changed situation.
- Protect important and urgent deadlines.
- Consider duration and available time.
- Do not invent tasks.
- Use exact task names.
"""

    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return json.loads(response.output_text)

    except Exception as e:

        return {
            "action": "WAIT",
            "task_order": [],
            "reason": f"AI replanning failed: {e}"
        }