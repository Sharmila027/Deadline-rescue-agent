from app.agent.agent import DeadlineRescueAgent
from app.agent.input_parser import parse_task
from app.tools.task_tool import add_task, get_tasks
from app.memory.memory import Memory



memory = Memory()
agent = DeadlineRescueAgent(memory)

print("\nDEADLINE RESCUE AGENT")

print("\nDescribe your tasks in natural language.")
print("Type 'done' when finished.")

while True:

    text = input("\nTask: ")

    if text.lower() == "done":
        break

    try:
        task = parse_task(text)

        add_task(
            task["name"],
            task["deadline"],
            task["duration"],
            task["importance"]
        )

        print("\nTask added:")
        print(task)

    except ValueError as e:
        print("\nError:", e)


print("\nYOUR TASKS")

for task in get_tasks():
    print(task)


print("\nAGENT ANALYSIS")

plan = agent.analyze()

print("\nINITIAL PLAN")

for item in plan:
    print(item)


print("\nSIMULATING CHANGE")

if get_tasks():

    changed_task = get_tasks()[0]["name"]

    new_plan = agent.handle_change(
        "The task is taking longer than expected",
        changed_task
    )

    print("\nUPDATED PLAN")

    for item in new_plan:
        print(item)


print("\nAGENT MEMORY")

for event in memory.get_history():
    print(event)


print("\nTEST COMPLETE")