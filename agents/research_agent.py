from ddgs.ddgs import DDGS  # <--- YAHAN CHANGE HAI

def search(query: str) -> str:
    """
    Searches the web for a given query using DuckDuckGo and returns the top 3 results.
    """
    print(f"--- [Real Agent Action]: Searching web for '{query}' ---")
    try:
        # Note: DDGS() ke andar ab koi parameter nahi hai
        results = list(DDGS().text(query, max_results=3))
        if not results:
            return "No information found."
        
        formatted_results = "\n".join([f"Title: {res['title']}\nSnippet: {res['body']}\n---" for res in results])
        return formatted_results
    except Exception as e:
        return f"An error occurred during web search: {e}"