#!/usr/bin/env bash
# проверка, что репозиторий готов к GitHub Pages (без git)
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

fail() { echo "check-pages-ready: $*" >&2; exit 1; }

test -f talk.html || fail "нет talk.html — запустите ./scripts/export-html.sh"
test -d talk_assets || fail "нет talk_assets/"
test -d playground || fail "нет playground/"
test -f .github/workflows/pages.yml || fail "нет workflow Pages"

UV_PYTHON_PREFERENCE=only-managed uv run python <<'PY'
import re, pathlib, subprocess, sys
root = pathlib.Path(".")
html = (root / "talk.html").read_text(encoding="utf-8")
refs = re.findall(r"talk_assets/([a-zA-Z0-9_./-]+\.mp4)", html)
missing = [r for r in refs if not (root / "talk_assets" / r).exists()]
if missing:
    print("missing videos:", *missing[:10], sep="\n  ")
    sys.exit(1)
if "Введение в λ-исчисление" not in html:
    sys.exit("unexpected <title> in talk.html")
if "site-nav" not in html:
    sys.exit("нет ссылки на playground — запустите export-html или patch-talk-site-nav")
low = []
for r in sorted(set(refs)):
    p = root / "talk_assets" / r
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=height", "-of", "csv=p=0", str(p)],
        text=True,
    ).strip()
    if int(out) < 1080:
        low.append(f"{r} ({out}p)")
if low:
    print("videos below 1080p:", *low[:12], sep="\n  ")
    sys.exit("перерендерите: ./scripts/render.sh <Scene…> && ./scripts/export-html.sh")
print(f"ok: {len(set(refs))} videos @1080p, title, nav")
PY

UV_PYTHON_PREFERENCE=only-managed uv run python <<'PY'
import json, pathlib, re, sys
from presentation import ORDER
slides = pathlib.Path("slides")
bad = []
for cls in ORDER:
    p = slides / f"{cls.__name__}.json"
    if not p.exists():
        continue
    if re.search(r"\n\s*480\s*\n", p.read_text()):
        bad.append(cls.__name__)
if bad:
    print("slides JSON still 480p:", ", ".join(bad))
    sys.exit(1)
print("ok: all scene JSON 1080p")
PY

"$root/scripts/build-pages.sh" "$root/_site"
test -f _site/index.html || fail "_site/index.html не создан"
test -d _site/playground || fail "_site/playground не создан"

echo "ready for git push: talk.html talk_assets/ playground/ .github/ scripts/ (+ исходники lc/ …)"
