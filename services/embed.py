import os
import json
import openai
from sqlalchemy.orm import Session
from services.models import SessionLocal, Metadata

# Ensure OPENAI_API_KEY is set in your environment
openai.api_key = os.getenv("OPENAI_API_KEY", "<YOUR_OPENAI_API_KEY>")

def embed_text(text: str):
    """Call OpenAI to embed a single text string."""
    resp = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return resp["data"][0]["embedding"]

def generate_and_store_embeddings():
    db: Session = SessionLocal()
    entries = db.query(Metadata).all()
    count = 0

    for entry in entries:
        # Combine fields into a single prompt
        prompt = f"{entry.query} | {entry.discogs} | {entry.youtube}"
        embedding = embed_text(prompt)

        # Store embedding on the Metadata record
        entry.embedding = embedding  # ensure your model has an embedding column
        count += 1

    db.commit()
    db.close()
    print(f"Stored embeddings for {count} entries.")

if __name__ == "__main__":
    generate_and_store_embeddings()
