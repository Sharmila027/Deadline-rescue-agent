from app.database.database import get_connection


def add_task(name, deadline, duration, importance=3):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks
        (name, deadline, duration, importance, completed)
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        deadline,
        duration,
        importance,
        0
    ))

    conn.commit()
    task_id = cursor.lastrowid

    conn.close()

    return {
        "id": task_id,
        "name": name,
        "deadline": deadline,
        "duration": duration,
        "importance": importance,
        "completed": False
    }


def get_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, deadline, duration, importance, completed
        FROM tasks
    """)

    rows = cursor.fetchall()

    conn.close()

    tasks = []

    for row in rows:

        tasks.append({
            "id": row[0],
            "name": row[1],
            "deadline": row[2],
            "duration": row[3],
            "importance": row[4],
            "completed": bool(row[5])
        })

    return tasks


def complete_task(name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tasks
        SET completed = 1
        WHERE name = ?
    """, (name,))

    success = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return success


def clear_tasks():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks")

    conn.commit()
    conn.close()