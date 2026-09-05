tasks = []


def add_task(name, deadline, duration, importance=3):
    task = {
        "name": name,
        "deadline": deadline,
        "duration": duration,
        "importance": importance,
        "completed": False
    }

    tasks.append(task)
    return task


def get_tasks():
    return tasks


def complete_task(name):
    for task in tasks:
        if task["name"] == name:
            task["completed"] = True
            return True

    return False