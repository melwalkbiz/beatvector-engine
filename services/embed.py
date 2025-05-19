cat > services/embed.py << 'EOF'
import os
import sys
import openai
from sqlalchemy.orm import Session
from services.models import SessionLocal, Metadata

# ---- Configuration ----
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY not set", file=sys.stderr)
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
        print(f"OpenAI error: {e}", file=sys.stderr)
        sys.exit(1)

# ---- Main pipeline ----
def generate_and_store_embeddings():
    db: Session = SessionLocal()
    entries = db.query(Metadata).all()
    if not entries:
        print("No entries found. Run services.store first.", file=sys.stderr)
        sys.exit(1)
    for entry in entries:
        prompt = f"{entry.query} | {entry.discogs} | {entry.youtube}"
        entry.embedding = embed_text(prompt)
    db.commit()
    db.close()
    print(f"✔️  Stored embeddings for {len(entries)} entries.")

if __name__ == "__main__":
    generate_and_store_embeddings()
EOF
