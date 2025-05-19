from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "BeatVector™ Crawler OK"}

@app.get("/search")
def search(query: str):
    """
    Demo stub: always return an empty list for Discogs search.
    """
    return {"results": []}

@app.get("/youtube")
def youtube_search(query: str, maxResults: int = 5):
    """
    Demo stub: always return an empty list for YouTube.
    """
    return {"videos": []}
