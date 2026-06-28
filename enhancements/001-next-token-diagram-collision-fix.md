# 001 — Next-Token Diagram: Collision Fix

**Status:** ✅ Superseded by [002](002-autoregression-cascade-redesign.md)
**Trigger:** User feedback — "THIS DID NOT COME OUT WELL" (with screenshot)
**Location:** Section "The Origin of LLMs" → "How do they actually work?"

## Problem

In the original next-token-prediction SVG, a dashed teal loop-back arrow swept across the whole figure and its arrowhead landed **directly on the explanatory text** ("then the whole process repeats…"), tangling the line with the words. The result looked broken.

## Change

Rebuilt the SVG (`viewBox 0 0 880 300`) to remove the collision:

- **Winner → blank:** a short "sample" arc connecting the top-probability bar (`blue · 0.62`) to the `?` slot, routed through the empty gap between the two columns — no text in its path.
- **Repeat indicator:** replaced the messy full-width loop with a compact circular ↻ refresh glyph plus a clearly separated caption, below a divider line, so no arrow crosses any text.
- Muted the non-winning probability bars so the winner stands out.
- Added a local SVG `marker` (`#ntp-arr`) instead of relying on a marker defined in another inline SVG.

## Outcome

The collision was fixed, but the diagram still only depicted a **single** prediction step — it didn't actually convey the autoregressive *loop*. This shortcoming led directly to enhancement [002](002-autoregression-cascade-redesign.md), which replaced this design.
