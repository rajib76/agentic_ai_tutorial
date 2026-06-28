# 007 — Anchor scroll offset + sticky sidebar that follows scrolling

**Status:** ✅ Done
**Trigger:** "When I click and it goes to the bottom and then I come up, it cuts the top. Also the side menu should move with scrolling."
**Artifact:** `agentic_genai_tutorial.html`

## Changes

### 1. Anchor jumps no longer cut the heading
Added a consistent scroll offset so a section/heading never lands flush against the very top edge when navigated to (via either the JS `scrollIntoView` or a native hash):
- `html { … scroll-padding-top: 28px; }`
- `section.chapter { … scroll-margin-top: 28px; }`
- `h2, h3 { … scroll-margin-top: 28px; }` (the TOC sub-links target `<h3>` elements)

`scroll-margin-top` is honored by `scrollIntoView`, so the JS navigation from enhancement 006 now leaves a 28px gap above the target.

### 2. Sidebar reliably follows the scroll
Reworked the sticky sidebar so it pins and follows correctly instead of being forced to full viewport height:
- `position: -webkit-sticky; position: sticky; top: 16px;` (small gap from the top; `-webkit-` prefix for older Safari)
- `max-height: calc(100vh - 32px); overflow-y: auto;` — sizes to its content, scrolls internally only if the list is taller than the viewport.

## Verification
- SVG 16/16; one script block; all anchors resolve.
- Local open: sidebar stays pinned while scrolling; clicking a TOC item lands the section with a comfortable top gap.

## Important caveat — hosting method
Both reported symptoms are classic signs that the tutorial is being **scrolled inside a fixed-height iframe/embed** (e.g. Hostinger Website Builder's "Embed/Custom HTML" widget or a WordPress HTML block). Inside such an iframe:
- `position: sticky` can't pin to the *outer* page, so the side menu won't follow the parent scroll.
- The small iframe viewport makes anchor jumps look like the top is "cut."

The in-file fixes above make the page correct **as a standalone document**. For the best result, host it standalone — upload `agentic_genai_tutorial.html` via Hostinger **File Manager** (or set it as its own page) and link to it directly, rather than pasting it into a drag-and-drop HTML widget. If embedding is required, the iframe needs `height` large enough for the content (or a resize script), since an iframe cannot make its content stick to the parent window.
