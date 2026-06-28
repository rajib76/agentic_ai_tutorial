"""
Lab 2 — Meaning as geometry: embeddings
========================================

An embedding turns a piece of text into a list of numbers (a vector) so that
texts with *similar meaning* land *close together* in space. "Close" is measured
with cosine similarity: 1.0 = same direction (very similar), 0.0 = unrelated.

This lab embeds a handful of sentences, prints the full similarity matrix, and
shows that the API ranks them by meaning — not by shared keywords.

Run:
    export OPENAI_API_KEY="sk-..."
    python lab2_embeddings.py
"""

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

# The sentences live in sample_data.py so Lab 4 (UMAP) can reuse the exact same
# set — the pairs that score "similar" here are the ones that cluster there.
from sample_data import SENTENCES

load_dotenv()  # load OPENAI_API_KEY from a .env file if present
client = OpenAI()  # reads OPENAI_API_KEY from the environment

EMBED_MODEL = "text-embedding-3-small"  # 1536-dimensional vectors, cheap & fast


def embed(texts: list[str]) -> np.ndarray:
    """Return an (n, d) matrix of L2-normalized embedding vectors."""
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    vecs = np.array([item.embedding for item in resp.data], dtype=np.float32)
    # Normalize so that a plain dot product equals cosine similarity.
    vecs /= np.linalg.norm(vecs, axis=1, keepdims=True)
    return vecs


if __name__ == "__main__":
    print("=" * 64)
    print("LAB 2 · Embeddings — meaning becomes geometry")
    print("=" * 64)

    vecs = embed(SENTENCES)
    sim = vecs @ vecs.T  # cosine similarity matrix (normalized dot products)

    print(f"\nEach sentence -> a {vecs.shape[1]}-dimensional vector.\n")
    print("Cosine similarity matrix (1.00 = identical meaning):\n")
    header = "      " + "".join(f"  S{j+1} " for j in range(len(SENTENCES)))
    print(header)
    for i in range(len(SENTENCES)):
        row = "".join(f" {sim[i, j]:.2f}" for j in range(len(SENTENCES)))
        print(f"  S{i+1} {row}")

    print("\nLegend:")
    for i, s in enumerate(SENTENCES):
        print(f"  S{i+1}: {s}")

    # Find the most similar *pair* of different sentences.
    np.fill_diagonal(sim, -1)  # ignore each sentence vs. itself
    i, j = np.unravel_index(np.argmax(sim), sim.shape)
    print(f"\nClosest pair: S{i+1} & S{j+1}  (cosine = {sim[i, j]:.2f})")
    print("Notice the paraphrase pairs (e.g. cat/kitten, market/shares) score")
    print("high even though they share almost no words — the model matches")
    print("MEANING, not keywords. That is what makes semantic search (and RAG)")
    print("possible. Lab 4 plots THESE SAME sentences so you can see them cluster.")
