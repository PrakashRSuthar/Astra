import os
from dotenv import load_dotenv

load_dotenv()

# --- Debug Configuration ---
# Isse False karne par saare extra messages (Inner Monologue) band ho jayenge.
# Development ke waqt ise True kar sakte hain.
DEBUG_MODE = False

# --- LLM Configuration ---
OLLAMA_MODEL = "phi4-mini:latest"
OLLAMA_BASE_URL = "http://localhost:11434"

# --- Project Configuration ---
PROJECT_NAME = "Astra"