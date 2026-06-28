# 009 — Per-section assignments & self-check quizzes

## Trigger
> "for each section, please add an assignment for students to try. For example for RAG, give an assignment to the students including some quiz questions"

## What changed
Added a `📝 Assignment` block at the end of **every** section of `agentic_genai_tutorial.html` (Sections 01–08), each containing a hands-on task plus a "Quick quiz — check yourself" with collapsible answers.

- **Section 01 (Big Picture):** classify systems into Rule-based AI / ML / GenAI / Not AI; 3 quiz Qs (ML⊃GenAI, discriminative vs generative, why "generative").
- **Section 02 (LLMs):** extend Lab 1 with own prompts, catch a hallucination; 4 Qs (what it predicts, tokens, hallucination, temperature).
- **Section 03 (Embeddings):** add a topic to `sample_data.py`, predict then check similarities, view cluster in Lab 4; 4 Qs (cosine, meaning-not-words, analogy arithmetic, UMAP caveats).
- **Section 04 (RAG):** *the richer one the user asked for* — replace `KNOWLEDGE_BASE` with own facts, test in-context / out-of-context / multi-chunk questions, break it with `k=1`, chunking stretch; 5 Qs (two phases, why grounding helps, chunk size, mismatched embedding models, fixing bad retrieval).
- **Section 05 (Agents):** design a ReAct loop on paper with tools + stop rule; 4 Qs (ReAct steps, what makes an agent, tool calling, stopping condition).
- **Section 06 (Multi-agent):** decompose a workflow into 3 specialized agents + pattern + failure mode; 4 Qs (autonomy ordering, patterns, advantage/risk, human checkpoint).
- **Section 07 (Use cases):** write a one-page agentic spec mapping parts back to sections; 3 Qs (common skeleton, support corpus, when not to use an agent).
- **Section 08 (Labs):** capstone wiring all four labs into one mini-app; 4 Qs (`max_completion_tokens`, autocomplete system prompt, no `top_k` in OpenAI, shared embedding space).

## Implementation notes
- New CSS (using existing tokens only — still fully self-contained): `.callout.assignment` (green accent), `.quiz-title`, `.callout ol/ul`, and `details`/`summary` styling for collapsible answers. `<details>`/`<summary>` are native HTML — no JS or external deps added.
- No new sections, so **no renumbering** and no anchor changes; assignments were inserted before each section's closing `</section>`, anchored to the next section's (unique) boundary comment.

## Follow-up — standalone RAG programming assignment
Trigger: "did you add a programming assignment also for RAG" → user chose a dedicated starter file with TODOs.
- Added `labs/assignments/rag_assignment.py` — scaffolded exercise: OpenAI calls + a chunkable document provided; student implements `chunk_document`, `embed`, `retrieve`, `answer` (each `raise NotImplementedError`). Built-in `check()` harness runs three questions (in-context / out-of-context refusal / two-far-apart-chunks) plus 4 reflection questions (k, chunk size, mismatched embedding model, why it refuses).
- Added `labs/assignments/rag_assignment_solution.py` — complete reference implementation (sentence-aware chunking verified offline to split the release-year and warranty facts into separate chunks so the two-fact question genuinely needs k≥2).
- `labs/README.md` gained a "Programming assignment" section; the HTML RAG assignment now links to the standalone exercise.
- All assignment scripts pass `py_compile`; chunking logic validated offline (no API).

## Validation
- 8 `callout assignment` blocks; `<details>`/`</details>` balanced 31/31.
- SVG 19/19; no external `src`/CDN/`@import`; all anchors resolve; `<section>` tags 9/9; display numbers contiguous 01–08 + Appendix A.
