from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agent.agent import DeadlineRescueAgent
from app.agent.input_parser import parse_task
from app.tools.task_tool import (
    add_task,
    get_tasks,
    clear_tasks,
    complete_task
)
from app.tools.calendar_tool import clear_events
from app.memory.memory import Memory
from app.database.database import init_db




app = FastAPI(
    title="Deadline Rescue Agent"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


memory = Memory()
agent = DeadlineRescueAgent(memory)

init_db()

class TaskInput(BaseModel):
    text: str


class ChangeInput(BaseModel):
    reason: str
    changed_task: str


class CompleteTaskInput(BaseModel):
    name: str


@app.get("/")
def home():

    return {
        "message": "Deadline Rescue Agent API is running"
    }


@app.get("/tasks")
def tasks():

    return get_tasks()


@app.post("/tasks")
def create_task(data: TaskInput):

    try:

        task = parse_task(data.text)

        add_task(
            task["name"],
            task["deadline"],
            task["duration"],
            task["importance"]
        )

        return {
            "message": "Task added successfully",
            "task": task
        }

    except ValueError as e:

        return {
            "error": str(e)
        }


@app.post("/tasks/complete")
def complete_task_endpoint(data: CompleteTaskInput):

    success = complete_task(data.name)

    if not success:

        return {
            "message": "Task not found"
        }

    return {
        "message": "Task completed successfully"
    }


@app.post("/analyze")
def analyze():

    plan = agent.analyze()

    return {
        "message": "AI plan created",
        "plan": plan
    }


@app.post("/replan")
def replan_schedule(data: ChangeInput):

    plan = agent.handle_change(
        data.reason,
        data.changed_task
    )

    return {
        "message": "Schedule replanned",
        "plan": plan
    }


@app.get("/memory")
def memory_history():

    return memory.get_history()


@app.delete("/tasks")
def clear_all_tasks():

    clear_tasks()
    memory.clear()
    clear_events()

    return {
        "message": "Tasks, agent memory and calendar events cleared"
    }


@app.post("/monitor")
def monitor_schedule():

    result = agent.monitor()

    return {
        "message": "Schedule monitoring completed",
        "alerts": result["alerts"],
        "replanned": result["replanned"],
        "plan": result["plan"]
    }