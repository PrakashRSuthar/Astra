from langchain_ollama import OllamaLLM  # <--- PEHLA CHANGE YAHAN
import config

def get_llm():
    """Initializes and returns the Ollama LLM instance."""
    if config.DEBUG_MODE:
        print("Connecting to LLM...")
    
    # Yahan bhi class ka naam badla hai
    llm = OllamaLLM(                 # <--- DOOSRA CHANGE YAHAN
        model=config.OLLAMA_MODEL,
        base_url=config.OLLAMA_BASE_URL,
        temperature=0.0,
        keep_alive="20m"
    )
    
    if config.DEBUG_MODE:
        print("LLM connection successful. Model will stay in memory for 20 minutes of inactivity.")
    
    return llm