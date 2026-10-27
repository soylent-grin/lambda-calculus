#!/usr/bin/env bash
# link to playground on exported slides (idempotent)
set -euo pipefail
file="${1:-talk.html}"
grep -q 'class="site-nav"' "$file" && exit 0
python3 - "$file" <<'PY'
import sys
path = sys.argv[1]
mark = "  </body>"
nav = """
    <style>
      .site-nav {
        position: fixed; bottom: 0.65rem; left: 0.75rem; z-index: 40;
        margin: 0; font: 0.78rem system-ui, sans-serif; opacity: 0.5;
        pointer-events: none;
      }
      .site-nav a { color: #58c4dd; text-decoration: none; pointer-events: auto; }
      .site-nav a:hover { opacity: 1; }
    </style>
    <p class="site-nav"><a href="playground/">Песочница →</a></p>
"""
text = open(path, encoding="utf-8").read()
if mark not in text:
    sys.exit(f"no {mark.strip()!r} in {path}")
open(path, "w", encoding="utf-8").write(text.replace(mark, nav + mark, 1))
PY
