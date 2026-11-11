#!/usr/bin/env python3
"""Link checker for docs/ — reports dead external URLs.

Scans all .md files under docs/ for http/https URLs, attempts a HEAD
request with a short timeout. Degrades gracefully when offline (reports
"unchecked" instead of crashing).

Usage: python3 tools/check_links.py [--timeout 5]
"""
from __future__ import annotations

import argparse
import pathlib
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

URL_RE = re.compile(r"https?://[^\s<>\"]+", re.IGNORECASE)
DEFAULT_TIMEOUT = 5


def find_urls(path: Path) -> list[str]:
    """Extract all http/https URLs from a markdown file."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []
    return URL_RE.findall(text)


def check_url(url: str, timeout: int) -> tuple[bool, str | None]:
    """HEAD request to check if URL is reachable. Returns (ok, error)."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "WorkspaceAlpha-link-check/1.0")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status < 400, None
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


def is_offline_error(error: str | None) -> bool:
    if error is None:
        return False
    offline_keywords = ["network", "unreachable", "timed out", "connection",
                        "no route", "host", "dns", "temporary failure"]
    return any(k in error.lower() for k in offline_keywords)


def main():
    ap = argparse.ArgumentParser(description="Check external links in docs/")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                    help=f"Request timeout in seconds (default {DEFAULT_TIMEOUT})")
    args = ap.parse_args()

    if not DOCS.exists():
        print(f"FAIL: docs directory not found: {DOCS}")
        sys.exit(1)

    # Collect all URLs
    url_locations: dict[str, list[str]] = {}
    for md_file in sorted(DOCS.rglob("*.md")):
        urls = find_urls(md_file)
        rel = str(md_file.relative_to(ROOT))
        for u in urls:
            # Clean trailing punctuation
            u = u.rstrip(".,);]")
            url_locations.setdefault(u, []).append(rel)

    unique_urls = sorted(url_locations.keys())
    print(f"Found {len(unique_urls)} unique URLs across docs/")

    if not unique_urls:
        print("PASS: no external links to check")
        return

    dead = []
    unchecked = []
    ok = []

    for url in unique_urls:
        ok_flag, error = check_url(url, args.timeout)
        if ok_flag:
            ok.append(url)
        elif is_offline_error(error):
            unchecked.append((url, error))
        else:
            dead.append((url, error))

    if ok:
        print(f"\nOK ({len(ok)}):")
        for u in ok[:10]:
            print(f"  {u}")
        if len(ok) > 10:
            print(f"  ... and {len(ok) - 10} more")

    if unchecked:
        print(f"\nUNCHECKED (offline, {len(unchecked)}):")
        for u, err in unchecked[:10]:
            print(f"  {u} ({err})")
        if len(unchecked) > 10:
            print(f"  ... and {len(unchecked) - 10} more")

    if dead:
        print(f"\nDEAD ({len(dead)}):")
        for u, err in dead:
            print(f"  {u} ({err})")
        for u, locs in url_locations.items():
            if any(d[0] == u for d in dead):
                print(f"    referenced in: {', '.join(locs)}")
        print(f"\nFAIL: {len(dead)} dead link(s)")
        sys.exit(1)

    if unchecked:
        print(f"\nPASS: all reachable links OK ({len(unchecked)} unchecked due to offline)")
    else:
        print(f"\nPASS: all {len(ok)} links reachable")


if __name__ == "__main__":
    main()
