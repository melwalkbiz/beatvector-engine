from fastapi import FastAPI, HTTPException
import os
import requests
from googleapiclient.discovery import build

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "<YOUR_YOUTUBE_KEY>")

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "BeatVector™ Crawler OK"}

@app.get("/search")
def search(query: str):
    # Uses Discogs API to fetch hip-hop metadata
    token = os.getenv("DISCOGS_TOKEN", "<YOUR_DISCOGS_TOKEN>")
    url = f"https://api.discogs.com/database/search?genre=hip-hop&q={query}&token={token}"
    response = requests.get(url)
    response.raise_for_status()
    results = response.json().get("results", [])
    return {"results": results}

@app.get("/youtube")
def youtube_search(query: str, maxResults: int = 5):
    """
    Fetches YouTube video metadata for the given query.
    """
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        req = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=maxResults,
            type="video"
        )
        res = req.execute()
        videos = []
        for item in res.get("items", []):
            videos.append({
                "title": item["snippet"]["title"],
                "videoId": item["id"]["videoId"]
            })
        return {"videos": videos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
