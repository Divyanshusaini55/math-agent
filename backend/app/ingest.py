# ingest.py
import asyncio
import uuid
from .vectorstore import upsert


async def seed():
    samples = [
        {"q": "Integrate x^2 dx", "a": "x^3/3 + C"},
        {"q": "Solve x^2 - 5x + 6 = 0", "a": "x=2,3"}
    ]
    for s in samples:
        doc_id = str(uuid.uuid4())
        await upsert(doc_id, s["q"] + "\nAnswer: " + s["a"], {"source":"seed"})
    print("Seeded KB.")

if __name__ == "__main__":
    asyncio.run(seed())
