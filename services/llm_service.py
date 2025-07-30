from langchain_groq import ChatGroq
import os

def get_llm():
    """Initializes and returns the ChatGroq model instance."""
    
    # Using Groq with the powerful Llama3 8b model. It's extremely fast and reliable.
    llm = ChatGroq(
        model="llama3-8b-8192",
        temperature=0.1,  # Thodi si creativity ke liye
        api_key=os.getenv("GROQ_API_KEY")
    )
    return llm