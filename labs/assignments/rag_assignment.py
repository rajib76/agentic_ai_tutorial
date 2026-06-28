"""
PROGRAMMING ASSIGNMENT — Build a RAG pipeline from scratch
==========================================================

Lab 3 handed you a finished RAG loop. Here you build one yourself. The OpenAI
calls and the data are provided; YOU implement the four core functions that turn
a document into grounded answers. Fill in every `TODO` (each `raise
NotImplementedError` marks a spot to replace).

THE PIPELINE YOU ARE BUILDING
-----------------------------
    DOCUMENT --chunk--> chunks --embed--> vectors  (ingestion, done once)
    question --embed--> q_vec --retrieve(top-k)--> context --answer--> grounded reply

WHAT TO DO
----------
1. Implement chunk_document(), embed(), retrieve(), and answer().
2. Run the file. The `check()` at the bottom runs three questions:
     - one answerable from the document  -> expect a correct, grounded answer
     - one NOT in the document           -> the model should say it doesn't know
     - one needing TWO chunks combined   -> retrieval must pull both
3. Experiment and answer the reflection questions in REFLECTION below.

GRADING-STYLE CHECKS (the file prints PASS/FAIL hints, but think about WHY).

Run:
    # OPENAI_API_KEY in a .env file at the repo root, or exported
    python labs/assignments/rag_assignment.py
"""

import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

# A short document to ground answers in. It is one blob of text ON PURPOSE — part
# of the assignment is splitting it into useful chunks. The "Aurora" facts are
# invented so the model cannot answer from training alone.
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
    """Split `text` into a list of smaller chunks.

    A simple, valid strategy: split into sentences, then group sentences so each
    chunk stays under ~max_words words. (Sentence-aware beats blind fixed-size
    because it keeps ideas intact.) Return a list of non-empty chunk strings.

    TODO: implement this. Hints:
      - split sentences on ". " (and re-add the period), or use a simple loop
      - accumulate words into the current chunk until it would exceed max_words
    """
    raise NotImplementedError("chunk_document: split DOCUMENT into chunks")


def embed(texts: list[str]) -> np.ndarray:
    """Return an (n, 1536) matrix of L2-NORMALIZED embedding vectors for `texts`.

    Normalizing means a plain dot product equals cosine similarity later.

    TODO: implement this. Hints:
      - call client.embeddings.create(model=EMBED_MODEL, input=texts)
      - stack [item.embedding for item in resp.data] into a numpy array
      - divide each row by its L2 norm: v / np.linalg.norm(v, axis=1, keepdims=True)
    """
    raise NotImplementedError("embed: return normalized embedding vectors")


def retrieve(question: str, chunks: list[str], chunk_vecs: np.ndarray,
             k: int = 2) -> list[str]:
    """Return the `k` chunks most similar to `question`.

    TODO: implement this. Hints:
      - embed the question (reuse embed([question])[0])
      - cosine similarity to every chunk = chunk_vecs @ q_vec  (vectors are normalized)
      - take the indices of the k highest scores (np.argsort(...)[::-1][:k])
      - return the corresponding chunk strings
    """
    raise NotImplementedError("retrieve: return the top-k chunks for the question")


def answer(question: str, context: list[str]) -> str:
    """Answer `question` using ONLY `context`. If the answer isn't there, the
    model should say it doesn't know.

    TODO: implement this. Hints:
      - build a prompt that includes the context lines and instructs the model to
        use ONLY that context and to say "I don't know" otherwise
      - call client.chat.completions.create(model=CHAT_MODEL, messages=[...],
        temperature=0)
      - return resp.choices[0].message.content.strip()
    """
    raise NotImplementedError("answer: build a grounded prompt and call the model")


# ---------------------------------------------------------------------------
# Provided: a small harness that exercises your pipeline. Don't edit (yet).
# ---------------------------------------------------------------------------
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


# ---------------------------------------------------------------------------
# REFLECTION — write your answers as comments here once the pipeline works.
# ---------------------------------------------------------------------------
# 1. Set k=1 in check(). The two-fact question (release year + warranty) now
#    loses half its answer — why? (Those facts live in two separate chunks, so
#    one retrieved chunk can't contain both.)
# 2. Set max_words very large so the WHOLE document becomes one chunk. Retrieval
#    now always returns everything. Why does that stop helping, and when (size of
#    corpus) would it start to hurt?
# 3. What would happen if you embedded the question with a DIFFERENT model than
#    the chunks? Why?
# 4. The "How much does it cost?" question isn't in the document. What made the
#    model refuse instead of inventing a price?

if __name__ == "__main__":
    print("=" * 64)
    print("ASSIGNMENT · Build a RAG pipeline (implement the TODOs)")
    print("=" * 64)
    check()
