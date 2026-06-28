# 000 — Initial Tutorial Build

**Status:** ✅ Done
**Trigger:** "CREATE THE TUTORIAL ON AGENTIC AND GENERATIVE AI" (via the `agentic_tutorial` skill)
**Artifact:** `agentic_genai_tutorial.html`

## What was built

A single, fully self-contained HTML tutorial (embedded CSS + JavaScript + inline SVG, no external/CDN dependencies) for developers new to generative and agentic AI. Original five content sections:

1. **The Origin of LLMs** — what an LLM is, the transformer/attention, the 3-stage build (pretraining → SFT → RLHF), tokenization, embeddings, next-token sampling, context window & knowledge cutoff, and hallucination as a consequence of next-token prediction.
2. **Grounding with RAG** — overview, the ingestion → retrieval → generation pipeline (rich diagram), embeddings/vector search/ANN, chunking strategies, retrieval strategies (dense, hybrid BM25, re-ranking).
3. **The Birth of Agents** — LLM core + planning + memory + tools, the ReAct loop, what agents add over plain LLMs, how to build one.
4. **Multi-Agent Orchestration** — the three autonomy patterns (deterministic workflow / controlled flow / controlled autonomy) mapped to a spectrum, plus the five canonical building blocks.
5. **Use Cases** — coding agents, deep research, customer support, computer-use, data/analytics agents — each with a flow diagram.

Plus Appendix A (References) and Appendix B (Glossary).

## Approach

- Dispatched **4 parallel research agents** to verify authoritative sources (papers + official docs) with currently-resolving URLs before writing — one agent per topic cluster (LLMs/hallucination, RAG/chunking, agents, multi-agent/use-cases).
- Reasoned through section completeness to ensure no significant concept was missed.

## Design system

- Dark theme, sticky table-of-contents sidebar, reading-progress bar, scroll-spy active-section highlight.
- Hand-authored inline SVG diagrams; concept cards; callouts (key/note/warn); comparison tables; pseudo-code blocks with manual syntax coloring.

## Sources

34 verified references (refs `[1]`–`[34]`), each an inline superscript link to a primary source (arXiv abstracts, official Anthropic/OpenAI/LangChain docs).

## Verification

- Programmatic checks: balanced `<svg>` tags, every `#refN` citation has a matching `id="refN"` target, no external `src`/CDN dependencies.
