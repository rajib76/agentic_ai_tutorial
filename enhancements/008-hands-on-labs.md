# 008 — Hands-On Labs (token probabilities, embeddings, UMAP, simple RAG)

## Trigger
> "for the tutorial, please also create some hands-on lab to show the token probabilities, embeddings a simple RAG, this needs to be handson, we will use openai models"

Follow-up during the same work:
> "also add a simple umap example to show how embeddings work"

## Scope decisions (confirmed with user)
- **Deliverable:** HTML section *and* runnable files (not HTML-only).
- **Environment:** plain Python scripts (`.py`), not notebooks.

## What changed

### New runnable lab files (repo `labs/` folder)
- `labs/requirements.txt` — `openai`, `numpy` (+ `umap-learn`, `matplotlib` for Lab 4).
- `labs/README.md` — setup, run commands, model list.
- `labs/lab1_token_probabilities.py` — calls `chat.completions.create(..., logprobs=True, top_logprobs=12, max_completion_tokens=1)` and prints the next-token probability distribution as an ASCII bar chart; contrasts a factual vs. open-ended prompt.
- `labs/lab2_embeddings.py` — embeds 5 sentences with `text-embedding-3-small`, normalizes, prints the cosine-similarity matrix, auto-detects the closest pair.
- `labs/lab3_simple_rag.py` — end-to-end RAG over an in-memory KB containing an invented fact ("Zephyr-9 error E7"); answers the same question without vs. with retrieval to show grounding.
- `labs/lab4_umap_embeddings.py` — embeds 18 words across 3 categories, runs `umap.UMAP(metric="cosine")` to 2-D, scatter-plots them coloured by category, writes `embeddings_umap.png`.

### New HTML section
- **Section 08 — "Hands-On Labs — Run It Yourself"** (`id="labs"`), inserted between Section 07 (Use Cases) and Appendix A (Glossary). **No renumbering required** — appended after the last numbered section, so existing display numbers and all anchor IDs are unchanged.
- Sub-anchors: `#labs-setup`, `#labs-tokens`, `#labs-emb`, `#labs-umap`, `#labs-rag`.
- Two new inline SVG diagrams:
  - A pipeline figure mapping each lab onto the path from text → grounded answer (markers `lab-arr`).
  - A mock UMAP scatter showing animals/fruits/countries in three colour-coded clusters (teal/amber/blue per the palette).
- Each lab has: a plain-language "why", a condensed syntax-highlighted code block, and a "Sample output" callout. Cross-links back to Sections 2, 3, 4.
- TOC updated with the Section 08 entry + 4 sub-items.

## Sources / verification
- A research subagent verified the OpenAI SDK details against current official docs before the code was finalized:
  - `logprobs=True` + `top_logprobs=N` (max **20**); response path `choices[0].logprobs.content[i].top_logprobs[j].{token,logprob,bytes}`; probability = `math.exp(logprob)`.
  - `text-embedding-3-small` valid, 1536-dim, batch list input via `response.data[i].embedding`.
  - `gpt-4o-mini` valid and supports logprobs.
  - `max_tokens` is deprecated but accepted; switched both the script and the HTML to **`max_completion_tokens`** for future-proofing.
  - `OpenAI()` reads `OPENAI_API_KEY` from the environment by default.
- Note: the tutorial's inline numbered references were removed in enhancement 005, so no `<ol class="refs">` entries were added; this section follows the current no-citation convention.

## Validation
- SVG balance: 18/18.
- No external `src`/CDN/`@import` (still fully self-contained).
- All in-page anchors resolve (TOC + cross-links).
- Section display numbers contiguous 01–08 + Appendix A.
- `python -m py_compile labs/*.py` — all four scripts compile.

## Follow-up refinements (same work session)
- **UMAP → interactive 3-D:** `lab4` rewritten to render a rotatable 3-D scatter (`plt.show()`), with `--2d` flag and PNG export; later given exhaustive line-by-line teaching comments. HTML run-line + README updated.
- **.env support:** added `python-dotenv` to requirements; all four labs call `load_dotenv()` before `OpenAI()`. Added `labs/.env.example` and README guidance. Deps installed into `.venv`.
- **Lab 1 — answers + sampling controls:** `lab1` now prints each prompt's actual answer (`answer()` helper) and explains temperature / top_p / top_k. HTML gained a 3-card explainer (noting OpenAI exposes temperature & top_p but not top_k).
- **Lab 1 — show probabilities changing:** sampling demo rewritten to fetch ONE real distribution and reshape it locally — `apply_temperature` (= `softmax(logprob/T)`), `apply_top_p` (nucleus), `apply_top_k` — printed as side-by-side probability tables. Math verified offline (T=0.25 sharpens 0.42→0.95; top_p/top_k keep nucleus and renormalize to sum 1).
- **Lab 1 — how temperature scales:** added the logits→softmax derivation (`p_i(T)=exp(z_i/T)/Σexp(z_j/T)`) in `apply_temperature`'s docstring plus a live 2-token worked example (z=[2,1] → 88/12, 73/27, 62/38). HTML gained a formula callout and a new SVG figure showing the same logits reshaped at T=0.5/1.0/2.0. (SVG count 18→19, balanced.)

- **Unify Lab 2 & Lab 4 data:** new `labs/sample_data.py` holds one themed sentence set (12 sentences, 4 topics: pets/finance/food/travel, with paraphrase pairs and short plot labels). Both `lab2_embeddings.py` and `lab4_umap_embeddings.py` now `from sample_data import ...` so the pairs that score "similar" in Lab 2 are the ones that cluster in Lab 4. (Lab 4 previously used unrelated single words; UMAP `n_neighbors` 5→4 for 12 points.) HTML Lab 4 code snippet + the UMAP figure were rebuilt to 4 topic clusters with sentence labels; README notes the shared module. Verified offline: 12 sentences / 12 labels / 12 groups stay index-aligned, 3 per topic.

## Not run
- The labs were **not executed** (they require a live `OPENAI_API_KEY` and network). They are syntax-checked and built against verified current API shapes; sample outputs in the HTML are illustrative.
