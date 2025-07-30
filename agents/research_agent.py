from langchain.tools import tool
from ddgs.ddgs import DDGS

@tool
def web_search(query: str) -> str:
    """Use this for general, factual, or evergreen information. Do NOT use for recent news or current events."""
    print(f"\n[🔎 Research Agent] working on: query='{query}'\n")
    try:
        results = list(DDGS().text(query, max_results=5))
        if not results:
            return "No information found."
        return "\n".join([f"Title: {res['title']}\nSnippet: {res['body']}\n---" for res in results])
    except Exception as e:
        return f"An error occurred during web search: {e}"