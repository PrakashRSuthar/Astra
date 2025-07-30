from langchain.tools import tool
from pydantic.v1 import BaseModel, Field
from services import llm_service

class WriterInput(BaseModel):
    text_to_process: str = Field(description="The block of text that needs to be processed.")
    task_instruction: str = Field(description="A clear instruction for the writing task, e.g., 'summarize this in 3 bullet points'.")

@tool("writer", args_schema=WriterInput)
def writer(text_to_process: str, task_instruction: str) -> str:
    """Use this tool to summarize, rephrase, or format a given block of text based on an instruction."""
    print(f"\n[📝 Writer Agent] working on: task='{task_instruction}'\n")
    llm = llm_service.get_llm()
    prompt = f'You are a skilled writer. Your task is to: "{task_instruction}".\n\nHere is the text you need to work on:\n---\n{text_to_process}\n---\n\nProvide ONLY the resulting text as your output.'
    try:
        response = llm.invoke(prompt)
        return response
    except Exception as e:
        return f"An error occurred in the Writer Agent: {e}"