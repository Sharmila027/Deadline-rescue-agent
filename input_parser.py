import re


def parse_task(text):

    text = text.strip()

    duration_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(hours|hour|hrs|hr)",
        text.lower()
    )

    deadline_match = re.search(
        r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}",
        text
    )

    if not duration_match:
        raise ValueError("Please provide estimated duration.")

    if not deadline_match:
        raise ValueError(
            "Please provide deadline as YYYY-MM-DD HH:MM"
        )

    duration = float(duration_match.group(1))
    deadline = deadline_match.group()

    importance = 3

    if "very important" in text.lower():
        importance = 5
    elif "important" in text.lower():
        importance = 4

    name = text.split("by")[0]

    name = re.sub(
        r"^(i need to|i have to|i want to)\s+",
        "",
        name.strip(),
        flags=re.IGNORECASE
    )

    name = re.sub(
        r"^(finish|complete|prepare for)\s+(my\s+)?",
        "",
        name.strip(),
        flags=re.IGNORECASE
    )

    name = name.strip().capitalize()

    return {
        "name": name,
        "deadline": deadline,
        "duration": duration,
        "importance": importance
    }