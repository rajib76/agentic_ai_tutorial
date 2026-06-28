# Hands-On Labs — Generative & Agentic AI

Three small, runnable Python scripts that turn the tutorial's core ideas into
something you can watch happen on your own machine. They use **OpenAI models**.

| Lab | File | What you'll see |
|-----|------|-----------------|
| 1 | `lab1_token_probabilities.py` | The probability distribution an LLM produces for its *next token* — confident facts spike, open-ended prompts spread out. |
| 2 | `lab2_embeddings.py` | Sentences turned into vectors; a cosine-similarity matrix showing the model matches *meaning*, not keywords. |
| 3 | `lab3_simple_rag.py` | A complete tiny RAG pipeline (embed → retrieve → grounded answer), proving retrieval beats the model's memory. |
| 4 | `lab4_umap_embeddings.py` | The vector space made visible — UMAP projects 1536-D embeddings to an interactive **3-D** scatter (`--2d` for flat). Uses the **same sentences as Lab 2** (`sample_data.py`); they cluster by topic. Saves a PNG too. |

> Labs 2 and 4 share their sentences via `sample_data.py`, so the pairs that score "similar" in Lab 2 are the ones you see cluster in Lab 4.

## Setup

```bash
# from the repo root
python -m venv .venv && source .venv/bin/activate   # if you don't already have one
pip install -r labs/requirements.txt

# get a key from https://platform.openai.com/api-keys, then EITHER:
#   (a) put it in a .env file (the scripts call load_dotenv automatically):
cp labs/.env.example .env && echo "OPENAI_API_KEY=sk-..." > .env
#   (b) or export it in your shell:
export OPENAI_API_KEY="sk-..."
```

Each script calls `load_dotenv()`, so a `.env` file in the directory you run from
(or any parent) is picked up automatically — no need to export the key each time.

## Run

```bash
python labs/lab1_token_probabilities.py
python labs/lab2_embeddings.py
python labs/lab3_simple_rag.py
python labs/lab4_umap_embeddings.py        # interactive 3-D vector space
python labs/lab4_umap_embeddings.py --2d    # flat 2-D version
```

## Programming assignment — build RAG from scratch

`assignments/rag_assignment.py` is a graded-style exercise: the OpenAI calls and
a small document are provided, and **you** implement the four core functions
(`chunk_document`, `embed`, `retrieve`, `answer`) marked with `TODO` /
`raise NotImplementedError`. A built-in harness then runs three questions — one
answerable from the document, one that isn't (the model should refuse), and one
that needs two far-apart chunks combined — and there are reflection questions to
work through (effect of `k`, chunk size, mismatched embedding models).

```bash
python labs/assignments/rag_assignment.py            # your version (fails until you fill the TODOs)
python labs/assignments/rag_assignment_solution.py   # complete reference solution
```

Try it before peeking at the solution.

## Models used

- **Chat:** `gpt-4o-mini` — small, cheap, supports `logprobs`.
- **Embeddings:** `text-embedding-3-small` — 1536-dimensional vectors.

These labs make a handful of API calls each; the cost is a fraction of a cent.
Read each file top-to-bottom — they're commented to be read as a lesson.
