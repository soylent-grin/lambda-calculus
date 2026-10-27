#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export UV_PYTHON_PREFERENCE=only-managed
args=("$@")
if [ ${#args[@]} -eq 0 ]; then
  args=(--fps 30 -r 1920,1080)
fi
mapfile -t names < <(uv run python -c 'from presentation import ORDER; print("\n".join(c.__name__ for c in ORDER))')
uv run manim-slides render "${args[@]}" presentation.py "${names[@]}"
