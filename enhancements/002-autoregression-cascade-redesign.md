# 002 — Autoregression: Unrolled Cascade Redesign

**Status:** ✅ Done
**Trigger:** User feedback — "CAN YOU NOT DO A BETTER JOB THAN THIS SHOWING THE AUTO REGRESSION" (with screenshot)
**Location:** Section "The Origin of LLMs" → "How do they actually work?"

## Problem

The previous diagram ([001](001-next-token-diagram-collision-fix.md)) showed only a single prediction over one blank. It never conveyed the essence of **autoregression**: that each predicted token is fed back in and the sequence grows step by step.

## Change

Replaced the SVG with an **unrolled cascade of 4 generation steps** (`viewBox 0 0 880 360`):

- **Step 1:** input `The sky is` → predicts **`blue`** (teal = just generated)
- **Step 2:** `The sky is blue` → predicts **`and`**
- **Step 3:** `The sky is blue and` → predicts **`clear`**
- **Step 4:** `The sky is blue and clear` → predicts the next token (`…`)

Key visual elements:

- **Feedback arrows** (dashed teal) curve from each predicted token down into the *same position* in the next row's input — literally showing "the output is fed back as input," labelled *"fed back as input."*
- Column headers (STEP / INPUT SEQUENCE / PREDICTS →) and per-step probability annotations (`p=.62`, etc.).
- A legend strip decoding teal (just predicted) vs. muted (existing context) boxes.
- Two local markers (`#ntp-arr`, `#ntp-grey`).

The `figcaption` was rewritten to describe autoregression unrolling over four steps.

## Outcome

The diagram now makes the generation **loop** explicit — the sequence visibly grows by one token each step — and is free of the earlier text-collision issue.
