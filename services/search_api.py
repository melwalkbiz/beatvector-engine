from fastapi import FastAPI, HTTPException
from qdrant_client import QdrantClient
import os

app = FastAPI()

@app.get("/search")
def search(query: str, limit: int = 10):
    """
    Stub: perform a vector search in Qdrant.
    """
    try:
        client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY")
        )
        # Placeholder vector; real implementation will generate a query embedding
        query_vector = [0.0] * 1536
        results = client.search(
            collection_name="hiphop",
            query_vector=query_vector,
            limit=limit
        )
        # Extract payloads from search results
        hits = [hit.payload for hit in results]
        return {"results": hits}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
