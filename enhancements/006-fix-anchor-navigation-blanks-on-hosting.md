# 006 — Fix: anchor links blank the page when hosted (Hostinger)

**Status:** ✅ Done
**Trigger:** "WHEN I ADD THIS IN HOSTINGER AND CLICK ON A LINK IT BLANKS OUT"
**Artifact:** `agentic_genai_tutorial.html`

## Diagnosis

Every link in the tutorial is an in-page anchor (`href="#s1"`, `#map`, …) — there are no external links, and the JS doesn't hide content. The blanking is therefore a **navigation** problem introduced by the hosting environment, not a content bug.

Root cause: when the file is served through Hostinger's Website Builder, a WordPress/custom-HTML block, an iframe embed, or anything that injects a `<base href="…">` tag, a bare `#anchor` link stops being a same-page scroll. The browser resolves it against the injected base URL and performs a **full navigation** to e.g. `https://yoursite/page#s1`, which reloads or 404s — showing a blank page. Locally (`file://`) there is no base tag, so it worked fine, which is why the bug only appeared after hosting.

## Fix

Made in-page navigation JavaScript-driven so it no longer depends on default hash navigation (and thus is immune to `<base>` tags, iframes, and builder routing):

```js
document.querySelectorAll('a[href^="#"]').forEach(function (a) {
  a.addEventListener('click', function (e) {
    var id = a.getAttribute('href').slice(1);
    if (!id) return;
    var el = document.getElementById(id);
    if (!el) return;            // unknown target → keep default behavior
    e.preventDefault();         // stop the base-relative full navigation
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});
```

Also hardened the existing script while in there:
- Progress bar guards against a divide-by-zero when the page doesn't scroll.
- Scroll-spy now resolves sections via `getElementById(href.slice(1))` instead of `querySelector(href)`, which is safer and consistent with the new handler.

No markup/visual changes; purely the inline `<script>` block.

## Verification

- SVG balance 16/16; exactly one `<script>`/`</script>` pair; click handler + `preventDefault` present.
- Local open confirms sidebar links smooth-scroll to their sections.

## If it still blanks after re-upload

The remaining possibilities are environment-level, not in the file:
1. **Embedded via a builder block/iframe** — re-upload the `.html` as a standalone file/page and link to it directly, rather than pasting it into a drag-and-drop HTML widget.
2. **A `<base>` tag added by the platform** — the JS fix above already neutralizes this for clicks; if deep-linking (loading `…#s1` directly) misbehaves, remove any platform-injected `<base>`.
3. Hard-refresh / clear cache after re-upload so the browser picks up the new script.
