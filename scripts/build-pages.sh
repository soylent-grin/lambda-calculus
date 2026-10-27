#!/usr/bin/env bash
# static bundle for GitHub Pages (run from repo root after render + export-html)
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
out="${1:-$root/_site}"
mkdir -p "$out"
test -f "$root/talk.html"
"$root/scripts/patch-talk-site-nav.sh" "$root/talk.html"
cp "$root/talk.html" "$out/index.html"
cp "$root/talk.html" "$out/talk.html"
cp -r "$root/playground" "$root/talk_assets" "$out/"
touch "$out/.nojekyll"
echo "Site ready: $out (index.html = слайды, /playground/ = песочница)"
