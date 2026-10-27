#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export UV_PYTHON_PREFERENCE=only-managed
mapfile -t names < <(uv run python -c 'from presentation import ORDER; print("\n".join(c.__name__ for c in ORDER))')
uv run manim-slides present "${names[@]}"
