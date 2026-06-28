# Enhancements Log

This folder records every enhancement made to **`agentic_genai_tutorial.html`** after its initial creation. Each entry captures *what* changed, *why* (the request that triggered it), and the *technical details* of the change, so the evolution of the tutorial is traceable.

| #   | Enhancement | Trigger | Status |
|-----|-------------|---------|--------|
| 000 | [Initial tutorial build](000-initial-tutorial-build.md) | "Create the tutorial on agentic and generative AI" | ✅ Done |
| 001 | [Next-token diagram — collision fix](001-next-token-diagram-collision-fix.md) | "This did not come out well" (arrow overlapped text) | ✅ Superseded by 002 |
| 002 | [Autoregression — unrolled cascade redesign](002-autoregression-cascade-redesign.md) | "Can you not do a better job showing the auto regression" | ✅ Done |
| 003 | [Embeddings section (high-school level)](003-embeddings-section.md) | "Add a section on embedding… explain like to a high school student" | ✅ Done |
| 004 | [The Big Picture — AI/ML landscape & why 'generative'](004-big-picture-ai-ml-landscape.md) | "Add a section to show where GenAI/Agentic AI fall in AI/ML and why it is called generative" | ✅ Done |
| 005 | [Remove the References section (size reduction)](005-remove-references-section.md) | "The tutorial has become too big, remove the references section" | ✅ Done |
| 006 | [Fix anchor links blanking the page when hosted](006-fix-anchor-navigation-blanks-on-hosting.md) | "When I add this in Hostinger and click on a link it blanks out" | ✅ Done |
| 007 | [Anchor scroll offset + sticky sidebar](007-scroll-offset-and-sticky-sidebar.md) | "It cuts the top when I come back up; the side menu should move with scrolling" | ✅ Done |
| 008 | [Hands-on labs (token probs, embeddings, UMAP, simple RAG)](008-hands-on-labs.md) | "create some hands-on lab to show the token probabilities, embeddings a simple RAG… we will use openai models" + "add a simple umap example" | ✅ Done |
| 009 | [Per-section assignments & self-check quizzes](009-per-section-assignments.md) | "for each section, please add an assignment for students to try… including some quiz questions" | ✅ Done |

## Conventions

- The single source artifact is `../agentic_genai_tutorial.html` (fully self-contained: embedded CSS, inline SVG, no external/CDN dependencies).
- Every concept in the tutorial is backed by an authoritative, URL-verified citation. New sections append references to the end of the reference list (so existing citation numbers never shift) and cite those new numbers inline.
- Section **display numbers** are renumbered when a section is inserted; internal anchor IDs (`#s1`, `#s2`, `#emb`, `#map`, …) are kept stable to avoid breaking sub-anchors.

## Current document structure (after all enhancements)

1. **Section 01 — The Big Picture** (`#map`) — where GenAI/Agentic AI sit in AI/ML; why "generative"
2. **Section 02 — The Origin of LLMs** (`#s1`)
3. **Section 03 — Embeddings, Explained Simply** (`#emb`)
4. **Section 04 — Grounding with RAG** (`#s2`)
5. **Section 05 — The Birth of Agents** (`#s3`)
6. **Section 06 — Multi-Agent Orchestration** (`#s4`)
7. **Section 07 — Use Cases of Agentic AI** (`#s5`)
8. **Section 08 — Hands-On Labs** (`#labs`) — runnable OpenAI labs: token probabilities, embeddings, UMAP, simple RAG (scripts in `../labs/`)
9. Appendix A — Glossary

> Note: the numbered References appendix and all inline citations were removed in enhancement 005 to reduce size. The pre-removal cited version is preserved at `../agentic_genai_tutorial.html.bak`.
