import json
import os
from models.task_model import Task

DATA_FILE = "data/tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        try:
            data = json.load(file)
            return [Task.from_dict(task) for task in data]
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4)
