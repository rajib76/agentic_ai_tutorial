"""
Lab 3 — A complete (tiny) RAG pipeline
======================================

RAG = Retrieval-Augmented Generation. Instead of trusting the model's memory,
we (1) embed a small knowledge base, (2) embed the user's question, (3) retrieve
the closest chunks by cosine similarity, and (4) ask the model to answer using
ONLY those chunks. This grounds the answer in real text and curbs hallucination.

To prove it works, the knowledge base contains a made-up fact the model cannot
know from training. We answer the same question twice — without RAG (it guesses
or refuses) and with RAG (it answers correctly from the retrieved context).

Run:
    export OPENAI_API_KEY="sk-..."
    python lab3_simple_rag.py
"""

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # load OPENAI_API_KEY from a .env file if present
client = OpenAI()  # reads OPENAI_API_KEY from the environment

EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

# --- A tiny "knowledge base". In a real system these come from your documents,
#     split into chunks. The Z…fact is invented so the model can't already know it.
KNOWLEDGE_BASE = [
    "The Zephyr-9 coffee machine was released by Aetheris Labs in March 2024.",
    "The Zephyr-9 brews a full carafe in 90 seconds using induction heating.",
    "The Zephyr-9 has a known issue: error code E7 means the water filter is missing.",
    "Aetheris Labs is headquartered in Lisbon, Portugal.",
    "The company's first product, the Zephyr-1, was a manual pour-over kettle.",
]


def embed(texts: list[str]) -> np.ndarray:
    """Return an (n, d) matrix of L2-normalized embeddings."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    vecs = np.array([item.embedding for item in resp.data], dtype=np.float32)
    vecs /= np.linalg.norm(vecs, axis=1, keepdims=True)
    return vecs


def retrieve(question: str, kb_vecs: np.ndarray, k: int = 2) -> list[str]:
    """Return the top-k knowledge-base chunks closest to the question."""
    q_vec = embed([question])[0]
    scores = kb_vecs @ q_vec          # cosine similarity to every chunk
    top_idx = np.argsort(scores)[::-1][:k]
    return [KNOWLEDGE_BASE[i] for i in top_idx]


def ask(question: str, context: list[str] | None) -> str:
    """Ask the chat model, optionally grounding it in retrieved context."""
    if context:
        ctx = "\n".join(f"- {c}" for c in context)
        prompt = (
            "Answer the question using ONLY the context below. "
            "If the answer is not in the context, say you don't know.\n\n"
            f"Context:\n{ctx}\n\nQuestion: {question}"
        )
    else:
        prompt = question
    resp = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return resp.choices[0].message.content.strip()


if __name__ == "__main__":
    print("=" * 64)
    print("LAB 3 · Retrieval-Augmented Generation, end to end")
    print("=" * 64)

    # Ingestion (done once): embed the whole knowledge base.
    kb_vecs = embed(KNOWLEDGE_BASE)
    print(f"\nIndexed {len(KNOWLEDGE_BASE)} chunks "
          f"as {kb_vecs.shape[1]}-dim vectors.")

    question = "What does error code E7 mean on the Zephyr-9?"
    print(f'\nQuestion: "{question}"')

    # --- 1) Baseline: NO retrieval. The model has never seen the Zephyr-9. ---
    print("\n[ Without RAG ] -------------------------------------------")
    print(ask(question, context=None))

    # --- 2) With RAG: retrieve, then answer from the retrieved context. ---
    hits = retrieve(question, kb_vecs, k=2)
    print("\n[ With RAG ] ----------------------------------------------")
    print("Retrieved context:")
    for h in hits:
        print(f"  • {h}")
    print("\nGrounded answer:")
    print(ask(question, context=hits))

    print("\nTakeaway: same model, same question. Retrieval is the difference")
    print("between a confident guess and a correct, source-backed answer.")
