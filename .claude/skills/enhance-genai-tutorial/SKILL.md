---
name: enhance-genai-tutorial
description: >-
  Use this skill whenever the user wants to add, modify, fix, or improve anything
  in the generative & agentic AI tutorial (agentic_genai_tutorial.html) — for example
  "add a section on X to the tutorial", "fix that diagram", "this chart didn't come out
  well", "redo the RAG visual", "add a glossary term", "explain X like I'm a beginner",
  or "update the references". Trigger this even when the user doesn't name the file,
  as long as they're clearly talking about the AI/ML tutorial we built. It encodes the
  established conventions: a single self-contained HTML file, URL-verified authoritative
  citations, append-only references, stable anchor IDs, careful section renumbering,
  high-quality hand-authored SVG diagrams, and logging every change under enhancements/.
---

# Enhancing the Generative & Agentic AI Tutorial

This skill maintains and extends **`agentic_genai_tutorial.html`** — a single, self-contained HTML tutorial for developers new to generative and agentic AI. The whole value of this tutorial is that it is *trustworthy and polished*: every concept cites a real authoritative source, diagrams actually illuminate the mechanism, and the document stays internally consistent as it grows. These conventions exist to protect those properties. Follow them so an enhancement never silently breaks a citation, an anchor, or the visual language.

## Before you touch anything

1. **Locate the artifact.** It lives at the project root: `agentic_genai_tutorial.html`. The change log lives in `enhancements/`. If you can't find the HTML, ask rather than guessing.
2. **Read the relevant region**, not the whole file blindly — it's large. Use the table-of-contents `<aside class="toc">` near the top to map section anchors, then read the target section.
3. **Understand the request as a teacher would.** The audience is a beginner. If the user asks to "explain X simply," lead with an everyday analogy and a picture before any jargon. Match the existing voice: warm, concrete, second-person, generous with "why."

## The five conventions (the heart of this skill)

### 1. One self-contained HTML file — no external dependencies
Everything ships inline: CSS in the `<style>` block, diagrams as inline `<svg>`, behavior in the inline `<script>`. **Never** add `<link>`/`<script src>` to a CDN, web font, or image URL — the file must render identically offline. Reuse the existing design tokens and component classes (see `references/design-system.md`) so new content is visually indistinguishable from the original.

### 2. Every concept needs a verified, authoritative citation
This is non-negotiable and it's why readers trust the tutorial. Before writing a new concept, **verify its sources** — don't cite from memory, because URLs rot and details drift.

- Dispatch one or more research subagents (general-purpose) to confirm each source's exact title, authors, year, and a **currently-resolving** URL. Prefer arXiv abstract pages, official docs (Anthropic/OpenAI/Google/LangChain), ACL Anthology, or canonical project pages. Run them in parallel when you have several independent topics.
- A good verification prompt: *"Confirm these canonical sources with accurate, currently-resolving URLs. For each return exact title, authors, year, canonical URL. Use web fetch/search to confirm each resolves. Flag anything unverified."*
- Cite inline as a superscript right after the claim:
  `<sup class="cite"><a href="#refNN">[NN]</a></sup>`
- End each section with a `<p class="src-line">` summary line listing that section's sources.

### 3. References are append-only
The reference list is numbered and those numbers are referenced by dozens of inline `<sup>` links. **Never insert into the middle of the list** — it would renumber everything and silently corrupt every later citation. Always **append** new `<li id="refNN">` entries at the end of `<ol class="refs">`, taking the next free number, and cite those new numbers from your new content. Match the existing entry format: `<b>Title.</b> <span class="auth">Authors (Year).</span> <a href="..." target="_blank" rel="noopener">short-url</a>`.

### 4. Anchor IDs are stable; only *display* numbers renumber
When you insert a new section, the visible "Section 0N" labels and the table-of-contents numbers shift — but the internal anchor IDs (`#s1`, `#s2`, `#emb`, `#map`, and their `#xxx-sub` children) must **not** change, because sub-anchors and cross-links depend on them. Give a new section a fresh, descriptive ID (e.g. `id="emb"`, `id="map"`); leave existing IDs alone. See `references/renumbering.md` for the exact, collision-safe procedure (edit `sec-num` spans in **descending** order, update the TOC, and fix in-body "Section N" prose references).

### 5. Log every change under `enhancements/`
After completing an enhancement, add a numbered markdown record in `enhancements/` (e.g. `005-<slug>.md`) and a row in `enhancements/README.md`. Each record states: the **trigger** (the user's request/feedback verbatim or close), **what changed** (sections, diagrams, refs), **sources added**, **renumbering** (a before/after table if sections moved), and **verification** results. This keeps the tutorial's evolution traceable and lets a future session understand prior decisions.

## Diagram quality bar

Diagrams are a major reason this tutorial works — hold them to a high standard. Lessons learned the hard way:

- **A diagram must show the actual mechanism, not a frozen snapshot of it.** When asked to illustrate a *process* or *loop* (autoregression, the ReAct loop, a pipeline), show it unrolling across steps or cycling — don't draw a single static state and hope the caption carries the idea. (The autoregression diagram was redone as a 4-step unrolled cascade for exactly this reason.)
- **Nothing may overlap.** Route every connector through empty space; never let an arrowhead or line land on text. Before finalizing, mentally trace each `<path>`/`<line>` and confirm its endpoints and curve clear all `<text>` and `<rect>` boxes. Give the `viewBox` enough height/width to breathe.
- **Define markers locally.** Put `<marker>` arrowheads in each SVG's own `<defs>` with a unique id (e.g. `id="ntp-arr"`); don't rely on a marker defined in a different inline SVG.
- **Use the palette as meaning.** Teal = the highlighted/active/just-produced element; muted navy = context/inputs; the brand blues/purple for stages; rose for human/escalation boundaries; green for final outputs. Color should encode role, not decorate.
- **Caption every figure** with `<figcaption>` that states the takeaway, and cite the source there if the diagram depicts a specific paper's idea.

See `references/design-system.md` for the SVG box/arrow patterns and exact color tokens.

## Workflow for a typical enhancement

1. **Clarify scope** only if genuinely ambiguous; otherwise proceed with sensible defaults and say what you assumed.
2. **Verify sources** in parallel subagents (convention 2) — kick these off early so they run while you draft.
3. **Draft the content/diagram** in the existing voice and design language.
4. **Insert it** at the right place; if it's a new top-level section, run the renumbering procedure (`references/renumbering.md`) and add its TOC entry + sub-anchors.
5. **Append references** (convention 3) and wire up the inline `<sup>` citations + the section's `src-line`.
6. **Validate** before claiming done (see below).
7. **Log the enhancement** (convention 5).
8. **Open it** for the user: `open agentic_genai_tutorial.html`.

## Validate before you claim success

Run a quick structural check and report the numbers — never assert "done" without evidence:

```bash
f=agentic_genai_tutorial.html
echo "SVG balance: $(grep -oc '<svg' $f)/$(grep -oc '</svg>' $f)"           # must be equal
echo "ref targets: $(grep -oc 'id=\"ref[0-9]*\"' $f) | cited: $(grep -oE 'href=\"#ref[0-9]+\"' $f | sort -u | wc -l)"
# every inline citation must have a matching reference target:
for n in $(grep -oE 'href="#ref[0-9]+"' $f | grep -oE '[0-9]+' | sort -un); do grep -q "id=\"ref$n\"" $f || echo "MISSING target ref$n"; done
# no external dependencies crept in:
grep -oE 'src="https?://|@import|cdn\.' $f | sort -u   # should print nothing
# every TOC/cross anchor resolves:
for h in $(grep -oE 'href="#[a-z0-9-]+"' $f | sed 's/href="#//;s/"//' | sort -u); do grep -q "id=\"$h\"" $f || echo "MISSING #$h"; done
```

Confirm: SVG tags balanced, every citation resolves, section display numbers are contiguous, no external `src`/CDN, all anchors resolve. If a diagram changed, also eyeball it in the browser for overlaps.

## Reference files

- `references/design-system.md` — color tokens, component classes (callouts, cards, grids, tables, code blocks), and reusable SVG box/arrow patterns. Read before writing any new HTML or SVG so it matches.
- `references/renumbering.md` — the exact, collision-safe procedure for inserting a section and shifting display numbers without breaking anchors or citations.

## Things that are easy to get wrong

- Citing from memory instead of verifying — leads to dead links and wrong years. Always verify.
- Inserting a reference mid-list — silently corrupts later citations. Append only.
- Renaming an existing anchor ID to match a new display number — breaks sub-links. IDs stay; only display numbers move.
- A diagram that names a paper's idea without citing it in the `figcaption`.
- Claiming completion without running the validation block.
