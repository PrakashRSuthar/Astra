from ddgs.ddgs import DDGS
import config

def get_news(query: str, region: str = "in-en") -> str:
    """
    Searches for recent news for a given query using DuckDuckGo News for the India-English region.
    """
    if config.DEBUG_MODE:
        print(f"--- [News Agent Log]: Searching news for '{query}' ---")
    
    try:
        # region='in-en' for India-English news
        results = list(DDGS().news(keywords=query, region=region, max_results=5))
        if not results:
            return "No recent news found for this topic."
        
        formatted_results = "\n".join([
            f"Title: {res['title']}\n"
            f"Source: {res['source']}\n"
            f"Snippet: {res['body']}\n---" 
            for res in results
        ])
        return formatted_results
    except Exception as e:
        return f"An error occurred during news search: {e}"