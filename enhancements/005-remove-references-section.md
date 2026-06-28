# 005 — Remove the References Section (size reduction)

**Status:** ✅ Done
**Trigger:** "THE TUTORIAL HAS BECOME TOO BIG, REMOVE THE REFERENCES SECTION"
**Artifact:** `agentic_genai_tutorial.html`

## What changed

To honor the request *and* keep the document internally consistent (no broken links), the entire citation apparatus was removed as a unit — not just the appendix, which would have orphaned ~80 inline links:

- **Removed Appendix A — References** (`<section id="refs">`, the `<ol class="refs">` of 45 entries) and its preceding comment.
- **Removed all 61 inline citation superscripts** (`<sup class="cite">…</sup>`) throughout every section.
- **Removed all 7 per-section "Sources for this section:" lines** (`<p class="src-line">…</p>`).
- **Removed the table-of-contents "References" entry** (`<li><a href="#refs">`).
- **Promoted the Glossary** from "Appendix B" to "Appendix A" (it is now the only appendix).
- **Updated 3 stale prose mentions** that referenced inline citations / the References section:
  - Hero lede: "…backed by a verifiable, authoritative source" → "…grounded in the foundational research and official documentation behind today's AI."
  - Hero pill: "🔗 25+ cited sources" → "🔗 Built on primary research."
  - Footer: "Every claim is cited to a primary, authoritative source listed in the References." → "…drawn from the foundational papers and official documentation behind modern AI."

## How it was done

Bulk regex passes with `perl -0777 -i` (61 superscripts + 7 source lines are impractical to edit one-by-one). A backup was taken first: **`agentic_genai_tutorial.html.bak`** (the pre-removal version — the only way to restore the inline citations, since they can't be reconstructed by hand). Delete it once you're happy with the result.

## Impact

- File size: **124,639 → ~104,400 bytes** (~20 KB / ~16% smaller); 1,326 → ~1,250 lines.
- The tutorial's *content* is unchanged — all 7 sections, diagrams, tables, and callouts remain. Only the citation/reference layer was stripped.

## Note / trade-off

This reverses the original "every concept has a verifiable, authoritative source shown inline" property in favor of a leaner document. The underlying sources still informed the content; they're simply no longer displayed. If a lighter-weight middle ground is wanted later, options include: a single compact "Further reading" list (≈10 key sources) instead of 45 numbered entries, or a collapsible `<details>` references block. The backup file preserves the full cited version.

## Verification

- Residue checks all zero: no `<sup class="cite">`, no `class="src-line"`, no `href="#ref"`, no `id="ref…"`, no `id="refs"`/`class="refs"`, no TOC refs entry, no stray empty `<sup>`.
- Structure intact: SVG balance 16/16; 8 sections (7 content + Glossary); single "Appendix A".
- Every remaining anchor resolves; no external/CDN dependencies.
