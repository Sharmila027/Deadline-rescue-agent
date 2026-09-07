from app.database.database import get_connection


def add_event(name, start, end):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO calendar_events
        (task_name, start_time, end_time)
        VALUES (?, ?, ?)
    """, (
        name,
        start,
        end
    ))

    conn.commit()

    event_id = cursor.lastrowid

    conn.close()

    print("[CALENDAR] Event added:", name)

    return {
        "id": event_id,
        "name": name,
        "start": start,
        "end": end
    }


def get_events():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, task_name, start_time, end_time
        FROM calendar_events
    """)

    rows = cursor.fetchall()

    conn.close()

    events = []

    for row in rows:

        events.append({
            "id": row[0],
            "name": row[1],
            "start": row[2],
            "end": row[3]
        })

    return events


def clear_events():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM calendar_events")

    conn.commit()
    conn.close()