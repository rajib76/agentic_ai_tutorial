"""
SOLUTION — Build a RAG pipeline from scratch
============================================

A complete, working implementation of rag_assignment.py. Try the assignment
yourself first; use this to check your approach or if you get stuck.

Run:
    python labs/assignments/rag_assignment_solution.py
"""

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

DOCUMENT = """
The Aurora-X3 is a portable solar generator released by Helios Devices in 2025.
It stores 2.4 kilowatt-hours of energy and can recharge fully from sunlight in
about five hours. The Aurora-X3 has three USB-C ports and two standard AC
outlets. A blinking red light on the Aurora-X3 means the battery temperature is
too high and the unit has paused charging to protect itself. Helios Devices is
based in Reykjavik, Iceland. Helios Devices offers a five-year warranty on the
Aurora-X3. The companion app lets you monitor charge level and schedule quiet hours.
""".strip()


def chunk_document(text: str, max_words: int = 20) -> list[str]:
    """Sentence-aware chunking: group whole sentences up to ~max_words each."""
    # Split into sentences, keeping the period.
    sentences = [s.strip() + "." for s in text.replace("\n", " ").split(". ")]
    sentences = [s.rstrip(".") + "." for s in sentences if s.strip(". ")]

    chunks, current, count = [], [], 0
    for sent in sentences:
        words = len(sent.split())
        if current and count + words > max_words:
            chunks.append(" ".join(current))
            current, count = [], 0
        current.append(sent)
        count += words
    if current:
        chunks.append(" ".join(current))
    return chunks


def embed(texts: list[str]) -> np.ndarray:
    """Return an (n, 1536) matrix of L2-normalized embedding vectors."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    vecs = np.array([item.embedding for item in resp.data], dtype=np.float32)
    vecs /= np.linalg.norm(vecs, axis=1, keepdims=True)
    return vecs


def retrieve(question: str, chunks: list[str], chunk_vecs: np.ndarray,
             k: int = 2) -> list[str]:
    """Return the k chunks most similar to the question."""
    q_vec = embed([question])[0]
    scores = chunk_vecs @ q_vec            # cosine similarity (vectors normalized)
    top_idx = np.argsort(scores)[::-1][:k]
    return [chunks[i] for i in top_idx]


def answer(question: str, context: list[str]) -> str:
    """Answer using ONLY the context; otherwise say we don't know."""
    ctx = "\n".join(f"- {c}" for c in context)
    prompt = (
        "Answer the question using ONLY the context below. "
        "If the answer is not in the context, say you don't know.\n\n"
        f"Context:\n{ctx}\n\nQuestion: {question}"
    )
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return resp.choices[0].message.content.strip()


def check() -> None:
    print("Chunking the document...")
    chunks = chunk_document(DOCUMENT)
    print(f"  -> {len(chunks)} chunks")
    for c in chunks:
        print(f"     • {c}")

    print("\nEmbedding + indexing chunks...")
    chunk_vecs = embed(chunks)

    tests = [
        ("What does a blinking red light mean on the Aurora-X3?",
         "in the document — expect a correct, grounded answer"),
        ("How much does the Aurora-X3 cost?",
         "NOT in the document — the model should say it doesn't know"),
        ("In what year was the Aurora-X3 released, and how long is its warranty?",
         "needs TWO facts from far-apart chunks — retrieval must pull both"),
    ]
    for q, note in tests:
        print(f'\nQ: {q}\n   ({note})')
        hits = retrieve(q, chunks, chunk_vecs, k=2)
        print("   retrieved:")
        for h in hits:
            print(f"     - {h}")
        print(f"   answer: {answer(q, hits)}")


if __name__ == "__main__":
    print("=" * 64)
    print("SOLUTION · RAG pipeline")
    print("=" * 64)
    check()
