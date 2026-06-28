# 004 — The Big Picture: AI/ML Landscape & Why "Generative"

**Status:** ✅ Done
**Trigger:** "can you also add a section to show where does generative and agentic ai fall in AI and ML and why it is called generative"
**Anchor:** `#map` — inserted as the new **Section 01**, before "The Origin of LLMs"

## What was added

A new opening section, **"The Big Picture — Where Generative & Agentic AI Fit,"** with three subsections and three diagrams:

1. **Nested fields** (`#map-nest`) — a concentric-rings SVG (AI ⊃ Machine Learning ⊃ Deep Learning ⊃ Generative AI ⊃ LLMs) with a color-matched legend, each field defined as a specialized subset of the one around it. A note explains that Agentic AI is deliberately *not* a ring.
2. **Why "generative"?** (`#map-why`) — a side-by-side SVG contrasting **discriminative** models (draw a boundary: "cat or dog?", "spam or not?") vs **generative** models (learn the pattern, produce a brand-new example), plus a 4-row comparison table and a callout tying "generative" back to next-token prediction (it *writes* new text → it generates).
3. **Where Agentic AI fits** (`#map-agentic`) — the key beginner insight that agentic AI is **not a new model type** but a system pattern: `Generative model (LLM) + planning/memory/tools = Agentic AI`, shown as a layered "equation" diagram. Closes with a roadmap callout.

## Sources added (refs 40–45, all URL-verified)

| Ref | Source |
|-----|--------|
| 40 | AIMA (definition of AI) — Russell & Norvig, 4th ed. (2020) |
| 41 | Deep Learning — Goodfellow, Bengio, Courville (2016), deeplearningbook.org |
| 42 | Deep Learning (Nature review) — LeCun, Bengio, Hinton (2015) |
| 43 | On Discriminative vs. Generative Classifiers — Ng & Jordan (NIPS 2001) |
| 44 | Generative Adversarial Networks (GANs) — Goodfellow et al. (2014), arXiv:1406.2661 |
| 45 | On the Opportunities and Risks of Foundation Models — Bommasani et al. (2021), arXiv:2108.07258 |

References were **appended** (40–45) so existing citation numbers did not shift.

## Renumbering

Inserting The Big Picture as Section 01 shifted everything by one:

| Section | Before | After |
|---------|--------|-------|
| The Big Picture | — | **01** (new) |
| The Origin of LLMs | 01 | 02 |
| Embeddings | 02 | 03 |
| Grounding with RAG | 03 | 04 |
| The Birth of Agents | 04 | 05 |
| Multi-Agent Orchestration | 05 | 06 |
| Use Cases | 06 | 07 |

Display numbers (`sec-num` spans), TOC labels/entries, and all in-body "Section N" cross-references were updated; internal anchor IDs (`#s1`, `#s2`, `#emb`, …) were kept stable.

## Verification

9 chapters; 16 balanced SVGs; 45 references, all cited with resolving targets; section numbers run 01→07; new anchors `#map`, `#map-nest`, `#map-why`, `#map-agentic` present; no broken TOC anchors; all body "Section N" references point to the correct renumbered sections.
