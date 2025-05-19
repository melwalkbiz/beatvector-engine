import json
from sqlalchemy.orm import Session
from services.models import SessionLocal, Metadata

def store_metadata(input_file="data/metadata.json"):
    # Load the JSON data
    with open(input_file, "r") as f:
        data = json.load(f)

    # Open a DB session
    db: Session = SessionLocal()

    # Insert each entry
    count = 0
    for entry in data:
        obj = Metadata(
            query=entry["query"],
            discogs=entry.get("discogs", []),
            youtube=entry.get("youtube", [])
        )
        db.add(obj)
        count += 1

    db.commit()
    db.close()
    print(f"Stored {count} metadata entries.")

if __name__ == "__main__":
    store_metadata()
