# Renumbering Procedure — inserting a section safely

Inserting a new top-level section shifts the **visible** numbers of every section after it. The risk is corruption: a careless renumber can break sub-anchors, the table of contents, or in-body cross-references. Follow this exact order. The guiding principle: **anchor IDs never change; only display numbers move.**

## What changes vs. what stays

| Element | Changes? |
|---------|----------|
| `<span class="sec-num">Section 0N</span>` display labels | ✅ shift +1 from the insertion point |
| TOC entry numbers (`1 · …`, `2 · …`) | ✅ shift +1 |
| In-body prose like "see Section 3" | ✅ update to new numbers |
| `id="s1"`, `id="emb"`, `id="map"`, `#xxx-sub` anchor IDs | ❌ never change |
| `href="#refNN"` citations / `id="refNN"` targets | ❌ never change |

## Step-by-step

### 1. Renumber the `sec-num` display labels — in DESCENDING order
If you edit ascending, you create duplicate strings mid-way (two "Section 03") and the next edit becomes ambiguous. Go highest-first so each `old_string` is unique at edit time. Example, inserting a new Section 01 when 6 sections exist:

```
"Section 06" → "Section 07"
"Section 05" → "Section 06"
"Section 04" → "Section 05"
"Section 03" → "Section 04"
"Section 02" → "Section 03"
"Section 01" → "Section 02"
```
Then the new section gets `<span class="sec-num">Section 01</span>`.

Note these use the zero-padded form `Section 0N`, which is distinct from in-body prose like `Section 3` (no zero) — so they won't collide with prose edits.

### 2. Update the table of contents
In `<aside class="toc">`, bump each existing entry's leading number and insert the new section's entry (with its sub-anchors) at the right position. The `href` values point at the **stable anchor IDs**, which do not change — only the visible "N · " prefix does.

### 3. Insert the new `<section>`
Give it a fresh descriptive `id` (e.g. `id="agents-eval"`), a `sec-num` span with its new number, and sub-section `id`s of the form `id="<sectionid>-<slug>"`. Place it at the correct position in the document body.

### 4. Fix in-body "Section N" prose references
Search the body for cross-references and update them to the new numbers:
```bash
grep -nE 'Section [0-9]' agentic_genai_tutorial.html | grep -v 'class="sec-num"'
```
Each hit is a prose mention like "RAG (Section 3) and tools (Section 4)" — update the digits to match the new layout. Watch for a single number that appears in multiple places meaning different sections; edit by surrounding context, not blind replace-all.

### 5. Validate
```bash
f=agentic_genai_tutorial.html
echo "display numbers:"; grep -oE 'Section 0[0-9]' $f          # must be contiguous 01..0N
for h in $(grep -oE 'href="#[a-z0-9-]+"' $f | sed 's/href="#//;s/"//' | sort -u); do grep -q "id=\"$h\"" $f || echo "MISSING #$h"; done
grep -nE 'Section [0-9]' $f | grep -v 'class="sec-num"'        # sanity-read each prose ref
```
Confirm the display numbers run 01..0N with no gaps or dupes, every anchor resolves, and each prose "Section N" points where you intend.

## Worked precedent
Two insertions already done this way:
- Embeddings inserted (became Section 03 at the time), bumping RAG→Agents→Multi-Agent→Use-Cases each +1.
- The Big Picture inserted as Section 01, bumping everything else +1 again to the current 01→07 layout.

In both, anchor IDs (`#s1`, `#s2`, `#emb`, `#map`, …) were left untouched and only display numbers + TOC + prose references moved. See `enhancements/003-*.md` and `enhancements/004-*.md` for the before/after tables.
