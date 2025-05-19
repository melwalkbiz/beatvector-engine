import os
import json
from qdrant_client import QdrantClient

def generate_embedding(text: str):
    """Placeholder: call AI service to get a vector"""
    return [0.0] * 1536

def embed_metadata(metadata: list):
    """Embed items and upload to Qdrant"""
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    for item in metadata:
        vector = generate_embedding(item.get("lyrics", ""))
        client.upsert(
            collection_name="hiphop",
            points=[{
                "id": item["id"],
                "vector": vector,
                "payload": item
            }]
        )

if __name__ == "__main__":
    # Example run
    with open("data/metadata.json") as f:
        data = json.load(f)
    embed_metadata(data)
