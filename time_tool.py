from datetime import datetime


def get_current_time():
    return datetime.now()


def hours_until(deadline):
    deadline = deadline.strip()

    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
    ]

    for fmt in formats:
        try:
            deadline_time = datetime.strptime(deadline, fmt)
            break
        except ValueError:
            deadline_time = None

    if deadline_time is None:
        raise ValueError("Invalid deadline. Use YYYY-MM-DD HH:MM")

    now = datetime.now()

    difference = deadline_time - now

    return max(0, difference.total_seconds() / 3600)