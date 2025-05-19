from fastapi import FastAPI
import os
import requests

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "BeatVector™ Crawler OK"}

@app.get("/search")
def search(query: str):
    # Uses Discogs API to fetch hip-hop metadata
    token = os.getenv("DISCOGS_TOKEN", "<YOUR_TOKEN>")
    url = f"https://api.discogs.com/database/search?genre=hip-hop&q={query}&token={token}"
    response = requests.get(url)
    response.raise_for_status()
    results = response.json().get("results", [])
    return {"results": results}
