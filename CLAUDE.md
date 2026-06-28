# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A teaching project, not an application. It has two deliverables that mirror each other:

1. **`agentic_genai_tutorial.html`** — a single, fully self-contained HTML tutorial for developers new to generative & agentic AI (embedded CSS, inline SVG diagrams, inline JS; **no external/CDN dependencies** — it must render identically offline). This is the primary product.
2. **`labs/`** — runnable Python counterparts to the tutorial's "Section 08 — Hands-On Labs", so readers can execute the concepts (token probabilities, embeddings, UMAP, RAG) against live OpenAI models.

`agentic_genai_tutorial.html.bak` is a pre-edit backup (the pre-references-removal version); don't treat it as a second source of truth.

## Editing the HTML tutorial — use the skill

**Any change to `agentic_genai_tutorial.html` must go through the `enhance-genai-tutorial` skill.** Invoke it even when the user doesn't name the file but is clearly talking about the tutorial. It encodes conventions that are easy to break silently:

- **Self-contained:** never add `<link>`/`<script src>`/`@import`/CDN/web-font/image URLs. Reuse the existing `<style>` design tokens and component classes.
- **Stable anchor IDs:** section IDs (`#map`, `#s1`, `#emb`, `#s2`–`#s5`, `#labs`, `#glossary`) and their sub-anchors are referenced by the TOC and cross-links. When inserting a section, the visible `sec-num` "Section 0N" *display* numbers shift, but **IDs never change**. Append new sections after the last numbered one when possible to avoid renumbering entirely.
- **References were removed** (enhancement 005): the file currently has no `<ol class="refs">` and no inline `<sup class="cite">` citations. Match that — don't reintroduce a citation system unless asked. (The skill still describes append-only references for when they exist.)
- **Diagrams:** hand-authored inline `<svg>`; show mechanisms unrolling/clustering rather than a frozen frame; define `<marker>` arrowheads locally per-SVG with unique ids; route connectors through empty space (no overlaps); color encodes role (teal = active/highlight, navy = context, amber = tools, rose = human boundary, green = output).
- **Log every change** in `enhancements/`: add a numbered `NNN-slug.md` record (trigger, what changed, sources, renumbering, verification) and a row in `enhancements/README.md`.

The skill's reference files (`references/design-system.md`, `references/renumbering.md`) are the authority on color tokens, component classes, SVG patterns, and the collision-safe renumbering procedure.

## Validate HTML before claiming done

Run this and report the numbers (don't assert success without it):

```bash
f=agentic_genai_tutorial.html
echo "SVG: $(grep -oc '<svg' $f)/$(grep -oc '</svg>' $f)"               # must be equal
grep -oE 'src="https?://|@import|cdn\.' $f | sort -u                    # must print nothing
for h in $(grep -oE 'href="#[a-z0-9-]+"' $f | sed 's/href="#//;s/"//' | sort -u); do \
  grep -q "id=\"$h\"" $f || echo "MISSING #$h"; done                   # every anchor resolves
grep -oE 'sec-num">[^<]*' $f                                            # display numbers contiguous
```

For a diagram change, also open it (`open agentic_genai_tutorial.html`) and eyeball for overlaps.

## The labs (`labs/`)

Plain standalone Python scripts (target: Python 3.12; a `.venv/` exists at the repo root).

```bash
.venv/bin/pip install -r labs/requirements.txt   # openai, numpy, python-dotenv, umap-learn, matplotlib
# provide the key via a .env file (scripts call load_dotenv()) or export it:
cp labs/.env.example .env   # then edit; or: export OPENAI_API_KEY="sk-..."

.venv/bin/python labs/lab1_token_probabilities.py   # next-token logprobs + temperature/top_p/top_k
.venv/bin/python labs/lab2_embeddings.py            # cosine-similarity matrix
.venv/bin/python labs/lab3_simple_rag.py            # embed → retrieve → grounded answer
.venv/bin/python labs/lab4_umap_embeddings.py       # interactive 3-D UMAP (add --2d for flat)
```

There is no test suite. Validate lab edits with a compile check and (where possible) offline logic checks that don't hit the API:

```bash
.venv/bin/python -m py_compile labs/*.py
```

### Lab architecture notes (the non-obvious parts)

- **`labs/sample_data.py` is shared by Lab 2 and Lab 4.** It holds one themed sentence set (4 topics × 3 sentences, with deliberate paraphrase pairs) exposed as index-aligned `SENTENCES` / `SHORT_LABELS` / `GROUPS` / `TOPICS`. The point is continuity: the pairs that score "similar" in Lab 2 are the ones that visibly cluster in Lab 4. Keep the lists aligned and keep both labs importing from here.
- **Models:** `gpt-4o-mini` for chat (supports `logprobs`; use `max_completion_tokens`, not the deprecated `max_tokens`), `text-embedding-3-small` for embeddings (1536-D). When touching OpenAI API shapes, verify against current docs rather than memory.
- **Chat-model caveat baked into Lab 1:** gpt-4o-mini *responds* rather than *continues* text, so the labs use an autocomplete system prompt (`COMPLETION_SYSTEM` / `messages_for()`) to make the next token actually be the answer. Preserve this when editing Lab 1.
- **Sampling math:** temperature/top_p/top_k are demonstrated by reshaping one real distribution locally (temperature = `softmax(logprob / T)`; top_p/top_k zero the tail and renormalize), because the API doesn't return "the distribution at T=2.0". OpenAI exposes temperature and top_p but **not top_k** — keep that distinction accurate in both code and prose.

## Keep the HTML and labs in sync

Section 08 of the tutorial documents the labs (condensed code snippets, sample output, diagrams). When you change a lab's behavior, models, or data, update the corresponding Lab block in the HTML (and vice-versa), then re-run both validations above.
