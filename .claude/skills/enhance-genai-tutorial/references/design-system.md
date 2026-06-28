# Design System — agentic_genai_tutorial.html

Read this before writing any new HTML or SVG so new content is visually indistinguishable from the original. All of this is already defined in the file's single `<style>` block; **reuse it, don't redefine it.**

## Color tokens (CSS variables on `:root`)

| Token | Value | Use |
|-------|-------|-----|
| `--bg` | `#0b1020` | page background |
| `--bg-soft` | `#121a30` | inline code background |
| `--panel` | `#161f38` | cards, callouts, pills |
| `--panel-2` | `#1b274a` | diagram boxes (muted/context) |
| `--ink` | `#e7ecf5` | primary text |
| `--ink-soft` | `#aab4cc` | body text |
| `--ink-faint` | `#76829e` | captions, faint labels |
| `--line` | `#28324f` | borders, dividers |
| `--brand` | `#6ea8fe` | blue — primary accent / stages |
| `--brand-2` | `#8b7bff` | purple — secondary accent |
| `--teal` | `#41d6c3` | highlight / active / just-produced |
| `--amber` | `#ffb454` | actions / tools / warnings |
| `--rose` | `#ff7a90` | human boundary / escalation |
| `--green` | `#5fd38d` | final outputs / success |
| `--code-bg` | `#0e1426` | code block background |
| `--mono` | (system mono stack) | code, equations, token labels |

**Semantic color rule for diagrams:** color encodes role, not decoration.
- teal = the highlighted/active/just-generated element
- muted navy (`#1b274a` fill, `#28324f` stroke) = inputs / existing context
- brand blue/purple = pipeline stages / the LLM core
- amber = tool calls / actions
- rose = human-in-the-loop / escalation
- green = final answer / success state

## Section skeleton

```html
<section class="chapter" id="UNIQUE-ID">
  <span class="sec-num">Section 0N</span>
  <h2>Title</h2>
  <p class="section-intro">One- or two-sentence framing of why this matters.</p>

  <h3 id="UNIQUE-ID-sub">Subsection</h3>
  <p>Body with an inline citation.<sup class="cite"><a href="#refNN">[NN]</a></sup></p>

  <!-- figures, cards, callouts, tables, pre/code as needed -->

  <p class="src-line">Sources for this section: Name <a href="#refNN">[NN]</a>, …</p>
</section>
```

## Reusable components

**Callouts** (4 flavors via modifier class):
```html
<div class="callout key">   <!-- or: note | warn | (none) -->
  <div class="tag">LABEL</div>
  <p>Body.</p>
</div>
```
Use `key` (teal) for the one big takeaway, `note` (purple) for asides, `warn` (amber) for caveats.

**Concept cards in a grid:**
```html
<div class="grid cols-3">   <!-- cols-2 | cols-3 | cols-4 (collapse to 1 col on mobile) -->
  <div class="card"><h4>🧭 Title</h4><p>Short explanation.</p></div>
</div>
```

**Figure with diagram:**
```html
<figure>
  <div class="diagram">
    <svg viewBox="0 0 W H" role="img" aria-label="describe the diagram">…</svg>
  </div>
  <figcaption>Takeaway sentence. Cite if it depicts a specific paper.<sup class="cite"><a href="#refNN">[NN]</a></sup></figcaption>
</figure>
```

**Table:** plain `<table><thead>…<tbody>…` — already styled.

**Code / pseudo-code:** `<pre><code>…</code></pre>` with manual syntax spans:
`<span class="c-kw">def</span>` (keyword), `c-str` (string), `c-com` (comment), `c-fn` (function), `c-num` (number).

**Reference entry** (append to `<ol class="refs">`):
```html
<li id="refNN"><b>Title.</b> <span class="auth">Authors (Year).</span>
  <a href="URL" target="_blank" rel="noopener">short-url</a></li>
```

## SVG patterns

**Local arrowhead marker** (one per SVG, unique id):
```html
<defs>
  <marker id="UNIQUE-arr" viewBox="0 0 10 10" refX="8" refY="5"
          markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="#6ea8fe"/>
  </marker>
</defs>
```

**A labeled node box** (two-line label):
```html
<rect x="X" y="Y" width="W" height="H" rx="10" fill="#1b274a" stroke="#28324f"/>
<text x="Xc" y="Y1" fill="#e7ecf5" font-size="13" text-anchor="middle">Title</text>
<text x="Xc" y="Y2" fill="#76829e" font-size="11" text-anchor="middle">subtitle</text>
```
Highlighted/active box: `fill="#16213d" stroke="#41d6c3" stroke-width="2"` with teal text.

**A connector:** `<line … marker-end="url(#UNIQUE-arr)"/>` for straight, `<path d="M.. C.." …/>` for curves. Dashed (`stroke-dasharray="5 4"`) reads as "feedback/optional"; solid as "main flow."

**Overlap discipline:** before finalizing, trace every connector's endpoints and curve and confirm they pass through empty space — never across a `<text>` run or through a box that isn't their endpoint. Increase the `viewBox` rather than cramming.

**Process/loop diagrams:** show the mechanism unrolling (multiple steps) or cycling (a loop back-edge), not a single frozen frame. Static snapshots fail to convey processes.

## Voice

Second person, warm, concrete. Lead with an analogy or picture, then the formal definition. Always explain *why*, not just *what*. Beginner audience — define jargon on first use.
