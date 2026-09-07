import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def parse_task(text):

    text = text.strip()

    if not text:
        raise ValueError("Please describe your task.")

    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not available."
        )

    client = OpenAI(api_key=api_key)

    today = datetime.now().strftime("%Y-%m-%d %H:%M")

    prompt = f"""
You are a task information extractor for a Deadline Rescue Agent.

Current date and time:
{today}

Extract:

1. task name
2. deadline
3. estimated duration in hours
4. importance from 1 to 5

User input:
{text}

Rules:
- Understand natural language.
- Convert relative dates into YYYY-MM-DD HH:MM.
- Convert times such as 5 PM into 17:00.
- "very important" = 5.
- "important" = 4.
- Otherwise = 3.
- Duration must be a number.
- Do not invent information.
- Missing deadline or duration must be null.

Return ONLY valid JSON:

{{
    "name": "task name",
    "deadline": "YYYY-MM-DD HH:MM",
    "duration": 3,
    "importance": 5
}}
"""

    try:

        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        task = json.loads(response.output_text)

        if not task.get("deadline"):
            raise ValueError(
                "Please provide a deadline as YYYY-MM-DD HH:MM."
            )

        if not task.get("duration"):
            raise ValueError(
                "Please provide estimated duration."
            )

        return task

    except Exception as e:

        error_text = str(e)

        if "429" in error_text or "rate_limit" in error_text:

            raise ValueError(
                "AI request limit reached. "
                "Please wait before trying another AI request."
            )

        raise ValueError(
            f"Could not understand the task: {e}"
        )