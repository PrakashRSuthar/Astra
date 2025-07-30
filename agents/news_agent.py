from langchain.tools import tool
from ddgs.ddgs import DDGS

@tool
def news_search(query: str) -> str:
    """Use this ONLY for finding recent news, headlines, or current events from the last few days."""
    print(f"\n[📰 News Agent] working on: query='{query}'\n")
    try:
        results = list(DDGS().news(keywords=query, region="in-en", max_results=5))
        if not results:
            return "No recent news found for this topic."
        return "\n".join([f"Title: {res['title']}\nSource: {res['source']}\nSnippet: {res['body']}\n---" for res in results])
    except Exception as e:
        return f"An error occurred during news search: {e}"