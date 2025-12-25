## Cyber toolkit (two containers, one workflow)

This repo provides:
- **Scrape container**: safe-by-default single-URL fetcher with optional Playwright rendering.
- **Recon container**: `nmap` profiles with standardized outputs.
- **One workflow**: everything writes artifacts into `./runs/` (gitignored).

### Requirements
- Docker + Docker Compose plugin (`docker compose`)
- Explicit authorization for any targets you scan/scrape

### Setup + run (10 steps)
1. **Clone/open this repo on your laptop**
   - Open the folder in Cursor or a terminal.

2. **Verify Docker is installed**

```bash
docker --version
docker compose version
```

3. **Build both images (scrape + recon)**

```bash
make build
```

4. **Put authorized scan targets into `targets/targets.txt`**
   - One target per line (IP/hostname/CIDR).

5. **Run an inventory scan (safe baseline)**

```bash
make nmap-inventory TARGETS=targets/targets.txt
```

6. **Confirm outputs were written**
   - Look under `runs/nmap/<timestamp>/inventory.{nmap,gnmap,xml}`

7. **Run a deep scan ONLY when authorized (requires explicit opt-in)**

```bash
DEEP_OK=1 make nmap-deep TARGETS=targets/targets.txt
```

8. **Run a scrape (requires an explicit allowlist)**
   - `ALLOW_HOSTS` is a hard safety guard (comma-separated).

```bash
make scrape URL=https://example.com ALLOW_HOSTS=example.com
```

9. **Run a rendered scrape for JS-heavy pages**

```bash
make scrape URL=https://example.com ALLOW_HOSTS=example.com RENDER=true
```

10. **Review scrape artifacts**
   - Look under `runs/scrape/<timestamp>/`:
     - `raw.html` (raw response/DOM)
     - `content.txt` (extracted readable text)
     - `meta.json` (allowlist + final URL + metadata)
     - `summary.json` (quick summary)

### Notes on safety defaults
- **Scraping** refuses to fetch unless the URL host matches `ALLOW_HOSTS` (supports subdomains).
- **Deep scanning** refuses to run unless `DEEP_OK=1` is set.
