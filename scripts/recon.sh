#!/usr/bin/env bash
set -euo pipefail

mode="${MODE:-inventory}"
targets="${TARGETS:-}"

if [[ -z "${targets}" ]]; then
  echo "ERROR: TARGETS env var required (path to targets file). Example:"
  echo "  make nmap-inventory TARGETS=targets/targets.txt"
  exit 2
fi

if [[ ! -f "/work/${targets}" ]]; then
  echo "ERROR: targets file not found at /work/${targets}"
  exit 2
fi

ts="$(date -u +%Y%m%dT%H%M%SZ)"
out_root="/work/runs/nmap/${ts}"
mkdir -p "${out_root}"

common_flags=(
  -Pn
  --reason
  --max-retries 2
  --host-timeout 10m
  -T3
)

if [[ "${mode}" == "inventory" ]]; then
  out_base="${out_root}/inventory"
  mkdir -p "$(dirname "${out_base}")"
  echo "Running nmap inventory scan (authorized targets only): ${targets}"
  nmap \
    -iL "/work/${targets}" \
    -sS \
    -sV --version-light \
    --top-ports 1000 \
    "${common_flags[@]}" \
    -oA "${out_base}"
  echo "OK: wrote ${out_base}.{nmap,gnmap,xml}"
  exit 0
fi

if [[ "${mode}" == "deep" ]]; then
  if [[ "${DEEP_OK:-}" != "1" ]]; then
    echo "REFUSING: MODE=deep requires explicit confirmation."
    echo "Set DEEP_OK=1 only if you are authorized to run deeper checks, e.g.:"
    echo "  DEEP_OK=1 make nmap-deep TARGETS=targets/targets.txt"
    exit 3
  fi
  out_base="${out_root}/deep"
  mkdir -p "$(dirname "${out_base}")"
  echo "Running nmap deep scan (authorized targets only): ${targets}"
  nmap \
    -iL "/work/${targets}" \
    -sS \
    -sV \
    -sC \
    -O --osscan-limit \
    -p- \
    --script-timeout 2m \
    "${common_flags[@]}" \
    -oA "${out_base}"
  echo "OK: wrote ${out_base}.{nmap,gnmap,xml}"
  exit 0
fi

echo "ERROR: unknown MODE='${mode}' (expected 'inventory' or 'deep')"
exit 2
