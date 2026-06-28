# 003 — Embeddings Section (High-School Level)

**Status:** ✅ Done
**Trigger:** "PLEASE ADD A SECTION ON EMBEDDING AND EXPLAIN EMBEDDING LIKE YOU WILL EXPLAIN TO A HIGH SCHOOL STUDENT"
**Anchor:** `#emb` — inserted between LLMs and RAG (logical: RAG depends on embeddings)

## What was added

A new section, **"Embeddings, Explained Simply,"** written for a beginner/high-school reader:

- **The hook** — "A computer can't read, so how does it know *happy* ≈ *joyful* but *happy* ≠ *brick*?"
- **The map analogy** — every word is a pin on a giant "meaning map"; similar meanings are neighbors; the model places the pins itself by noticing the company words keep (Firth: *"You shall know a word by the company it keeps."*).
- **A "meaning map" SVG** — clusters for **Animals**, **Fruits**, and a **Royalty/Gender** parallelogram showing `man→king` parallel to `woman→queen`, with directions labeled "royalty" and "gender."
- **Meaning as math** — the `king − man + woman ≈ queen` equation, explained as arithmetic on coordinates; note that real embeddings have hundreds/thousands of dimensions (flattened to 2-D for intuition).
- **How similarity is measured** — cosine similarity ("same direction = same meaning"), with a tiny code example (`happy`/`joyful` ≈ 0.94 vs `happy`/`brick` ≈ 0.05).
- **Why it matters** — sentence/document embeddings (Sentence-BERT) power semantic search, RAG, and agent memory; three concept cards + a forward-looking callout.

Sub-anchors: `#emb-map`, `#emb-math`, `#emb-why`.

## Sources added (refs 35–39, all URL-verified)

| Ref | Source |
|-----|--------|
| 35 | word2vec — Mikolov et al. (2013), arXiv:1301.3781 |
| 36 | Linguistic Regularities (king−man+woman≈queen) — Mikolov, Yih, Zweig (NAACL 2013), ACL N13-1090 |
| 37 | GloVe — Pennington, Socher, Manning (EMNLP 2014) |
| 38 | Sentence-BERT — Reimers & Gurevych (2019), arXiv:1908.10084 |
| 39 | Distributional hypothesis — J. R. Firth (1957) |

References were **appended** (35–39) so existing citation numbers did not shift.

## Renumbering

Inserting Embeddings as Section 03 bumped: RAG → 03, Agents → 04, Multi-Agent → 05, Use Cases → 06. (These were later bumped again by [004](004-big-picture-ai-ml-landscape.md).) Internal anchor IDs were kept stable; only display numbers, TOC labels, and in-body "Section N" cross-references changed.

## Verification

Balanced SVGs; new anchors present; refs 35–39 each cited with a matching target; no broken TOC anchors; section numbers contiguous.
