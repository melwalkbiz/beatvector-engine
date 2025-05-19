import os
import sys
import json
import openai
from sqlalchemy.orm import Session
from services.models import SessionLocal, Metadata

# ---- Configuration ----
# Must set this in shell before running:
# export OPENAI_API_KEY=sk-...
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key.startswith("your_"):
    print("ERROR: You must set a valid OPENAI_API_KEY in your environment.", file=sys.stderr)
    sys.exit(1)
openai.api_key = api_key

# ---- Embedding function ----
def embed_text(text: str):
    try:
        resp = openai.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        return resp["data"][0]["embedding"]
    except Exception as e:
        print(f"OpenAI embedding error: {e}", file=sys.stderr)
        sys.exit(1)

# ---- Main pipeline ----
def generate_and_store_embeddings():
    db: Session = SessionLocal()
    entries = db.query(Metadata).all()
    if not entries:
        print("No metadata entries found. Make sure you ran services.store first.")
        sys.exit(1)

    for entry in entries:
        prompt = f"{entry.query} | {json.dumps(entry.discogs)} | {json.dumps(entry.youtube)}"
        embedding = embed_text(prompt)
        entry.embedding = embedding

    db.commit()
    db.close()
    print(f"✔️  Stored embeddings for {len(entries)} entries.")

if __name__ == "__main__":
    generate_and_store_embeddings()
