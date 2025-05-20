# services/crawler.py
from fastapi import FastAPI, HTTPException
import os, requests
from googleapiclient.discovery import build

app = FastAPI()
DISCOGS_TOKEN = os.getenv("DISCOGS_TOKEN", "<YOUR_DISCOGS_TOKEN>")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "<YOUR_YOUTUBE_API_KEY>")

@app.get("/health")
def health():
    return {"status": "BeatVector™ Crawler OK"}

@app.get("/search")
def search(query: str):
    # 1) Discogs call
    d_url = "https://api.discogs.com/database/search"
    d_params = {"genre": "hip-hop", "q": query, "token": DISCOGS_TOKEN}
    d = requests.get(d_url, params=d_params)
    d.raise_for_status()
    discogs_results = d.json().get("results", [])

    # 2) YouTube call
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        req = youtube.search().list(q=query, part="snippet", maxResults=5, type="video")
        resp = req.execute()
        yt_items = []
        for it in resp.get("items", []):
            s = it["snippet"]
            yt_items.append({
                "title": s["title"],
                "videoId": it["id"]["videoId"],
                "channel": s["channelTitle"],
                "publishedAt": s["publishedAt"]
            })
    except Exception as e:
        yt_items = []
        print("YouTube fetch error:", e)

    return {"discogs": discogs_results, "youtube": yt_items}
