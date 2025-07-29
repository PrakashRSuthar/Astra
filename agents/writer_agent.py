from services import llm_service

def process_text(text_to_process: str, task_instruction: str) -> str:
    """
    Uses the LLM to perform a specific writing task (e.g., summarize, rephrase) on a given text.
    """
    print(f"--- [Writer Agent Action]: Performing task '{task_instruction}' ---")
    
    # Is specific kaam ke liye LLM ko call karna
    llm = llm_service.get_llm()
    
    # Writer agent ke liye ek dedicated prompt
    prompt = f"""
    You are a skilled writer. Your task is to: "{task_instruction}".

    Here is the text you need to work on:
    --- START OF TEXT ---
    {text_to_process}
    --- END OF TEXT ---

    Please provide ONLY the resulting text as your output, without any extra commentary.
    """
    
    try:
        response = llm.invoke(prompt)
        return response
    except Exception as e:
        return f"An error occurred in the Writer Agent: {e}"