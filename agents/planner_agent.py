from langchain.tools import tool
from pydantic.v1 import BaseModel, Field

class AddTaskInput(BaseModel):
    task: str = Field(description="The detailed description of the task to add.")
    due_date: str = Field(description="The due date for the task, e.g., 'tomorrow', 'this Friday', 'August 5th'.", default="Not specified")

TASKS_FILE = "tasks.txt"

@tool("add_task", args_schema=AddTaskInput)
def add_task(task: str, due_date: str) -> str:
    """Use this tool to add a new task to your to-do list. Always include a task description."""
    print(f"\n[🗓️ Planner Agent] working on: adding task='{task}' with due_date='{due_date}'\n")
    try:
        # 'a' mode appends to the file. If the file doesn't exist, it creates it.
        with open(TASKS_FILE, "a") as f:
            f.write(f"- {task} (Due: {due_date})\n")
        return f"Successfully added the task: '{task}' to your to-do list."
    except Exception as e:
        return f"An error occurred while adding the task: {e}"

@tool
def view_tasks() -> str:
    """Use this tool to view all the tasks currently in your to-do list."""
    print(f"\n[🗓️ Planner Agent] working on: viewing tasks\n")
    try:
        with open(TASKS_FILE, "r") as f:
            tasks = f.read()
        if not tasks:
            return "You have no pending tasks in your list."
        return f"Here are your pending tasks:\n{tasks}"
    except FileNotFoundError:
        # If the file doesn't exist, it means there are no tasks yet.
        return "You haven't added any tasks yet."
    except Exception as e:
        return f"An error occurred while viewing tasks: {e}"