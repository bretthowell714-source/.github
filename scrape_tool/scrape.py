import argparse
import asyncio
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import httpx
import tldextract
import trafilatura
from bs4 import BeautifulSoup


@dataclass(frozen=True)
class ScrapeResult:
    url: str
    final_url: str
    status_code: int | None
    fetched_at_utc: str
    render: bool
    title: str | None
    text_chars: int


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _normalize_allow_hosts(value: str) -> list[str]:
    parts = [p.strip().lower() for p in value.split(",")]
    parts = [p for p in parts if p]
    deduped = sorted(set(parts))
    return deduped


def _host_allowed(host: str, allow_hosts: list[str]) -> bool:
    host = host.lower().strip(".")
    for allowed in allow_hosts:
        allowed = allowed.lower().strip(".")
        if host == allowed:
            return True
        if host.endswith("." + allowed):
            return True
    return False


def _assert_scope(url: str, allow_hosts: list[str]) -> None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL scheme must be http or https")
    if not parsed.hostname:
        raise ValueError("URL must include a hostname")

    if not _host_allowed(parsed.hostname, allow_hosts):
        raise PermissionError(
            f"Refusing to fetch '{url}' because host '{parsed.hostname}' "
            f"is not in ALLOW_HOSTS={','.join(allow_hosts)}"
        )

    # Extra guard: stop obvious localhost/link-local unless explicitly allowlisted.
    if re.match(r"^(localhost|127\.|0\.0\.0\.0|169\.254\.)", parsed.hostname, re.I):
        if not _host_allowed(parsed.hostname, allow_hosts):
            raise PermissionError("Refusing localhost/link-local without explicit allowlist")


async def _fetch_with_playwright(url: str) -> tuple[str, str]:
    from playwright.async_api import async_playwright  # imported lazily

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        resp = await page.goto(url, wait_until="networkidle", timeout=60_000)
        html = await page.content()
        final_url = page.url
        await browser.close()

        if resp is None:
            return html, final_url
        return html, final_url


def _fetch_plain(url: str) -> tuple[str, str, int]:
    headers = {
        "User-Agent": "cyber-toolkit-scraper/1.0 (authorized research; contact: local)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    with httpx.Client(
        timeout=httpx.Timeout(30.0, connect=10.0),
        follow_redirects=True,
        headers=headers,
    ) as client:
        r = client.get(url)
        r.raise_for_status()
        return r.text, str(r.url), r.status_code


def _extract_title_and_text(html: str, base_url: str) -> tuple[str | None, str]:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else None

    extracted = trafilatura.extract(html, url=base_url)
    if extracted:
        text = extracted.strip()
    else:
        text = soup.get_text("\n", strip=True)
    return title, text


def main() -> int:
    ap = argparse.ArgumentParser(description="Safe-by-default single-URL scraper (authorized use only).")
    ap.add_argument("--url", required=True, help="URL to fetch (http/https).")
    ap.add_argument(
        "--allow-hosts",
        required=True,
        help="Comma-separated allowlist of hosts/domains (hard safety guard). Example: example.com,sub.example.com",
    )
    ap.add_argument("--out-dir", required=True, help="Directory to write artifacts into.")
    ap.add_argument("--render", action="store_true", help="Render with Playwright (Chromium).")
    args = ap.parse_args()

    allow_hosts = _normalize_allow_hosts(args.allow_hosts)
    if not allow_hosts:
        print("ERROR: allow-hosts parsed empty; refusing.", file=sys.stderr)
        return 2

    try:
        _assert_scope(args.url, allow_hosts)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 3

    os.makedirs(args.out_dir, exist_ok=True)

    fetched_at = _utc_now()
    status_code: int | None = None

    try:
        if args.render:
            # Validate host again after redirects by verifying registrable domain similarity.
            # (We still record final_url and rely on allowlist check below.)
            html, final_url = asyncio.run(_fetch_with_playwright(args.url))
            parsed_final = urlparse(final_url)
            if parsed_final.hostname:
                _assert_scope(final_url, allow_hosts)
            status_code = None
        else:
            html, final_url, status_code = _fetch_plain(args.url)
            _assert_scope(final_url, allow_hosts)
    except httpx.HTTPStatusError as e:
        print(f"ERROR: HTTP error: {e}", file=sys.stderr)
        return 4
    except Exception as e:
        print(f"ERROR: fetch failed: {e}", file=sys.stderr)
        return 5

    out = Path(args.out_dir)
    (out / "raw.html").write_text(html, encoding="utf-8", errors="replace")

    title, text = _extract_title_and_text(html, final_url)
    (out / "content.txt").write_text(text, encoding="utf-8", errors="replace")

    # Avoid network fetches for suffix list inside isolated/offline environments.
    extractor = tldextract.TLDExtract(suffix_list_urls=None)
    ext = extractor(urlparse(final_url).hostname or "")
    registrable = ".".join([p for p in [ext.domain, ext.suffix] if p]) or None

    meta = {
        "url": args.url,
        "final_url": final_url,
        "status_code": status_code,
        "fetched_at_utc": fetched_at,
        "render": bool(args.render),
        "allow_hosts": allow_hosts,
        "registrable_domain": registrable,
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")

    result = ScrapeResult(
        url=args.url,
        final_url=final_url,
        status_code=status_code,
        fetched_at_utc=fetched_at,
        render=bool(args.render),
        title=title,
        text_chars=len(text),
    )
    (out / "summary.json").write_text(json.dumps(asdict(result), indent=2, sort_keys=True), encoding="utf-8")

    print(json.dumps(asdict(result), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

