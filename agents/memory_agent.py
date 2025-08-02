from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
import json
import os

MEMORY_FILE = "memory.json"

def _load_memory():
    """Helper function to load memories from the JSON file."""
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {} # Return empty dict if file is corrupted or empty

def _save_memory(memory_data):
    """Helper function to save memories to the JSON file."""
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_data, f, indent=2)

class SaveMemoryInput(BaseModel):
    key: str = Field(description="A simple, descriptive key for the memory, e.g., 'favorite_color' or 'friend_rohan_location'.")
    value: str = Field(description="The piece of information to remember.")

@tool("save_memory", args_schema=SaveMemoryInput)
def save_memory(key: str, value: str) -> str:
    """Use this tool to save a specific piece of information about the user for future reference."""
    print(f"\n[🧠 Memory Agent] working on: saving memory key='{key}'\n")
    memory = _load_memory()
    memory[key] = value
    _save_memory(memory)
    return f"Okay, I've remembered that '{key}' is '{value}'."

@tool
def recall_memory(key: str) -> str:
    """Use this tool to recall a specific piece of information from your memory using its key."""
    print(f"\n[🧠 Memory Agent] working on: recalling memory for key='{key}'\n")
    memory = _load_memory()
    value = memory.get(key)
    if value:
        return f"Recalled from memory: The value for '{key}' is '{value}'."
    else:
        return f"I don't have any memory stored for the key: '{key}'."

@tool
def view_all_memories() -> str:
    """Use this to get a list of everything you currently remember about the user."""
    print(f"\n[🧠 Memory Agent] working on: viewing all memories\n")
    memory = _load_memory()
    if not memory:
        return "I don't have any memories saved yet."
    
    # Format the memories into a nice string
    formatted_memories = "\n".join([f"- {key}: {value}" for key, value in memory.items()])
    return f"Here is everything I remember:\n{formatted_memories}"