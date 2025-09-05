# searcher.py
import os
import httpx
from dotenv import load_dotenv
load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY", None)

async def web_search(query: str, top_k=3):
    if not SERPER_API_KEY:
        return [{"source": "none", "snippet": "Web search not configured."}]
    return [{"source": "serper", "snippet": f"Result for {query}"}]
