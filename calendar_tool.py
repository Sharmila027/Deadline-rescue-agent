events = []


def add_event(name, start, end):
    event = {
        "name": name,
        "start": start,
        "end": end
    }

    events.append(event)

    print("[CALENDAR] Event added:", name)

    return event


def get_events():
    return events


def clear_events():
    events.clear()