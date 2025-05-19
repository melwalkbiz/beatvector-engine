from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "BeatVector™ Search OK"}

@app.get("/search")
def search(query: str, limit: int = 10):
    """
    Demo stub: returns empty results without Qdrant.
    """
    try:
        # In a real build, we'd query Qdrant here.
        return {"results": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
