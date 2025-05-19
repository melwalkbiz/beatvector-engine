cat > services/embed.py << 'EOF'
import os
import openai
from sqlalchemy.orm import Session
from services.models import SessionLocal, Metadata

# Load your key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY", "<YOUR_OPENAI_API_KEY>")

def embed_text(text: str):
    """Call OpenAI to embed a single text string using v1 API."""
    resp = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return resp["data"][0]["embedding"]

def generate_and_store_embeddings():
    db: Session = SessionLocal()
    entries = db.query(Metadata).all()
    count = 0

    for entry in entries:
        prompt = f"{entry.query} | {entry.discogs} | {entry.youtube}"
        embedding = embed_text(prompt)
        entry.embedding = embedding
        count += 1

    db.commit()
    db.close()
    print(f"Stored embeddings for {count} entries.")

if __name__ == "__main__":
    generate_and_store_embeddings()
EOF
