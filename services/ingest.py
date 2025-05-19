import os
import json
import requests

# Ensure YOUTUBE_API_KEY and DISCOGS_TOKEN are set in env
BASE_URL = "http://127.0.0.1:8000"

def fetch_discogs(query):
  resp = requests.get(f"{BASE_URL}/search", params={"query": query})
  resp.raise_for_status()
  return resp.json().get("results", [])

def fetch_youtube(query):
  resp = requests.get(f"{BASE_URL}/youtube", params={"query": query})
  resp.raise_for_status()
  return resp.json().get("videos", [])

def ingest_metadata(queries, output_file="data/metadata.json"):
  all_data = []
  for q in queries:
    discogs = fetch_discogs(q)
    yt = fetch_youtube(q)
    all_data.append({
      "query": q,
      "discogs": discogs,
      "youtube": yt
    })
  os.makedirs(os.path.dirname(output_file), exist_ok=True)
  with open(output_file, "w") as f:
    json.dump(all_data, f, indent=2)
  print(f"Wrote metadata for {len(queries)} queries to {output_file}")

if __name__ == "__main__":
  # Example keywords
  queries = ["Run-DMC", "Public Enemy", "A Tribe Called Quest"]
  ingest_metadata(queries)
