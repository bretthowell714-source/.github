#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${URL:-}" ]]; then
  echo "ERROR: URL env var required. Example:"
  echo "  make scrape URL=https://example.com ALLOW_HOSTS=example.com"
  exit 2
fi

if [[ -z "${ALLOW_HOSTS:-}" ]]; then
  echo "ERROR: ALLOW_HOSTS env var required (comma-separated). This is a hard safety guard."
  echo "Example:"
  echo "  make scrape URL=https://example.com ALLOW_HOSTS=example.com"
  exit 2
fi

ts="$(date -u +%Y%m%dT%H%M%SZ)"
out_dir="/work/runs/scrape/${ts}"
mkdir -p "${out_dir}"

render="${RENDER:-}"
args=()
if [[ "${render}" == "1" || "${render}" == "true" || "${render}" == "TRUE" ]]; then
  args+=(--render)
fi

python /work/scrape_tool/scrape.py \
  --url "${URL}" \
  --allow-hosts "${ALLOW_HOSTS}" \
  --out-dir "${out_dir}" \
  "${args[@]}"

echo "OK: wrote scrape artifacts to ${out_dir}"
