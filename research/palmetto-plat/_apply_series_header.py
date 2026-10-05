#!/usr/bin/env python3
"""Add the Palmetto Plat series line, badge, title and footer note.

The moved Urban Productivity pages predate the collection convention and each
has its own header and footer markup, so nothing can be matched structurally
across all four. The banner is therefore self-contained with inline styles and
is inserted straight after <body>; it needs nothing from the page's own CSS
and cannot disturb its layout.

Per the research-page directive: change nothing else in these pages.

Idempotent — re-running does not stack banners.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# slug -> (title, format label, number)
PAGES = {
    "ledgers/charleston-by-the-acre": ("Charleston by the Acre", "Ledgers", 2),
    "ledgers/capitals-ledger": ("The Capital's Ledger", "Ledgers", 3),
    "ledgers/brighton-question": ("The Brighton Question", "Ledgers", 4),
    "atlases/chapin-connected": ("Chapin, Connected", "Atlases", 2),
}

MARK = "pp-series-line"

BANNER = """
<div class="{mark}" style="font-family:Inter,system-ui,-apple-system,sans-serif;
  font-size:12px;letter-spacing:.08em;text-transform:uppercase;
  padding:10px 20px;border-bottom:1px solid rgba(128,128,128,.25);
  display:flex;flex-wrap:wrap;gap:8px 14px;align-items:center;">
  <a href="/research/palmetto-plat/" style="color:#C9A227;text-decoration:none;
    font-weight:600;">Palmetto Plat</a>
  <span style="opacity:.65;border:1px solid rgba(128,128,128,.4);border-radius:20px;
    padding:2px 10px;font-size:11px;">{label}, No. {number}</span>
</div>
"""

FOOTER_NOTE = (
    '<p class="{mark}-foot" style="font-family:Inter,system-ui,sans-serif;'
    'font-size:13px;opacity:.75;margin-top:18px;">'
    '{title} is No. {number} in {label}, part of '
    '<a href="/research/palmetto-plat/" style="color:#C9A227;">Palmetto Plat</a> '
    'from <a href="/research/" style="color:#C9A227;">Carolina Redesign Research</a>.'
    "</p>"
)


def apply(path: Path, title: str, label: str, number: int) -> str:
    html = path.read_text(encoding="utf-8", errors="replace")
    if MARK in html:
        return "already applied"

    banner = BANNER.format(mark=MARK, label=label, number=number)
    new, n = re.subn(r"(<body[^>]*>)", r"\1" + banner, html, count=1)
    if not n:
        return "NO <body> — skipped"
    html = new

    # Title: {Title} | {Format} No. {N} | Palmetto Plat
    html = re.sub(
        r"<title>.*?</title>",
        f"<title>{title} | {label} No. {number} | Palmetto Plat</title>",
        html, count=1, flags=re.S,
    )

    note = FOOTER_NOTE.format(mark=MARK, title=title, number=number, label=label)
    if "</footer>" in html:
        html = html.replace("</footer>", note + "\n</footer>", 1)
    else:
        html = html.replace("</body>", note + "\n</body>", 1)

    # The old back-link wording still says "Urban Productivity".
    html = re.sub(r"(←\s*)Urban Productivity", r"\1Palmetto Plat", html)

    path.write_text(html, encoding="utf-8")
    return "updated"


def main() -> int:
    for slug, (title, label, number) in PAGES.items():
        page = ROOT / slug / "index.html"
        if not page.exists():
            print(f"  MISSING {page}")
            continue
        print(f"  {slug:40} {apply(page, title, label, number)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
