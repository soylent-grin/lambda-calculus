#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export UV_PYTHON_PREFERENCE=only-managed
exec uv run python -m http.server --directory playground 8765
