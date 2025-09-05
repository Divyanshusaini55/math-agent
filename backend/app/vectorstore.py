# vectorstore.py
import os
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
import httpx
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)
COLLECTION = os.getenv("QDRANT_COLLECTION", "mathkb")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

def ensure_collection(dim=1536):
    try:
        client.get_collection(collection_name=COLLECTION)
    except Exception:
        client.recreate_collection(
            collection_name=COLLECTION,
            vectors_config=rest.VectorParams(size=dim, distance=rest.Distance.COSINE),
        )

async def embed_text(text: str) -> np.ndarray:
    if not GEMINI_API_KEY:
        return np.random.normal(size=(1536,)).astype(np.float32)
    # Replace URL with Gemini embeddings endpoint
    async with httpx.AsyncClient(timeout=30) as client_http:
        return np.random.normal(size=(1536,)).astype(np.float32)

async def upsert(doc_id: str, text: str, metadata: dict):
    vec = await embed_text(text)
    ensure_collection(dim=vec.shape[0])
    client.upsert(
        collection_name=COLLECTION,
        points=[
            rest.PointStruct(id=doc_id, vector=vec.tolist(), payload={"text": text, **metadata})
        ],
    )

def search_similar(vec: np.ndarray, top_k=3):
    ensure_collection(dim=vec.shape[0])
    res = client.search(collection_name=COLLECTION, query_vector=vec.tolist(), limit=top_k)
    results = []
    for hit in res:
        payload = hit.payload or {}
        results.append({
            "id": hit.id,
            "score": hit.score,
            "text": payload.get("text", ""),
            "meta": {k: v for k, v in payload.items() if k != "text"}
        })
    return results
