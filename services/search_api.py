# services/search_api.py
from fastapi import FastAPI, HTTPException
import os
import requests

app = FastAPI()

# By default we’ll call your crawler on port 8000
CRAWLER_BASE = os.getenv("CRAWLER_URL", "http://127.0.0.1:8000")

@app.get("/health")
def health():
    return {"status": "BeatVector™ Search OK"}

@app.get("/search")
def search(query: str):
    """
    Proxy the query to the crawler service and return its JSON.
    """
    try:
        resp = requests.get(
            f"{CRAWLER_BASE}/search",
            params={"query": query},
            timeout=5,
        )
        resp.raise_for_status()
        return resp.json()          # this already has {"discogs":…, "youtube":…}
    except requests.exceptions.RequestException as e:
        # turn any HTTP or network error into a 502 bad gateway
        raise HTTPException(status_code=502, detail=str(e))
