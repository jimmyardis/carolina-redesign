#!/usr/bin/env python3
"""Airtable report-queue helper for the /build-assessment skill.

The intake webhook (app.py, on Railway) writes each Vapi end-of-call to the
Assessments table with Status = "Ready for Report". This script is the local
side of that queue:

    python fetch_intakes.py list                          # pending intakes
    python fetch_intakes.py pull recXXXXXXXXXXXXXX        # save intake JSON locally
    python fetch_intakes.py mark recXXXXXXXXXXXXXX "Report Ready"

Credentials: AIRTABLE_TOKEN / AIRTABLE_BASE_ID / AIRTABLE_TABLE from the
environment, falling back to ~/.env.

Pulled intakes land in ../intakes/ (gitignored — this repo is public GitHub
Pages; client transcripts must never be pushed).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import httpx

PENDING_STATUS = "Ready for Report"
INTAKES_DIR = Path(__file__).resolve().parent.parent / "intakes"


def _load_env() -> dict[str, str]:
    cfg = {}
    env_file = Path.home() / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            m = re.match(r"^(AIRTABLE_[A-Z_]+)=(.*)$", line.strip())
            if m:
                cfg[m.group(1)] = m.group(2).strip().strip("'\"")
    cfg.update({k: v for k, v in os.environ.items() if k.startswith("AIRTABLE_")})
    token = cfg.get("AIRTABLE_TOKEN", "")
    base = cfg.get("AIRTABLE_BASE_ID", "")
    if not (token and base):
        sys.exit("AIRTABLE_TOKEN / AIRTABLE_BASE_ID not set (env or ~/.env)")
    return {
        "token": token,
        "base": base,
        "table": cfg.get("AIRTABLE_TABLE", "Assessments"),
    }


def _client(cfg: dict[str, str]) -> httpx.Client:
    return httpx.Client(
        base_url=f"https://api.airtable.com/v0/{cfg['base']}",
        headers={"Authorization": f"Bearer {cfg['token']}"},
        timeout=30.0,
    )


def cmd_list(cfg: dict[str, str]) -> None:
    with _client(cfg) as c:
        resp = c.get(
            f"/{cfg['table']}",
            params={"filterByFormula": f"{{Status}} = '{PENDING_STATUS}'"},
        )
        resp.raise_for_status()
    records = resp.json().get("records", [])
    if not records:
        print(f"No intakes with Status = '{PENDING_STATUS}'.")
        return
    for r in records:
        f = r.get("fields", {})
        print(
            f"{r['id']}  {f.get('Business Name', 'Unknown'):<30}"
            f"  {f.get('Contact First Name', ''):<12}"
            f"  {f.get('Duration (s)', '?')}s  created {r.get('createdTime', '')[:10]}"
        )


def cmd_pull(cfg: dict[str, str], record_id: str) -> None:
    with _client(cfg) as c:
        resp = c.get(f"/{cfg['table']}/{record_id}")
        resp.raise_for_status()
    rec = resp.json()
    f = rec.get("fields", {})
    try:
        structured = json.loads(f.get("Structured Data", "{}"))
    except json.JSONDecodeError:
        structured = {"_raw": f.get("Structured Data", "")}

    business = f.get("Business Name", "unknown")
    slug = re.sub(r"[^a-z0-9]+", "-", business.lower()).strip("-") or "unknown"
    INTAKES_DIR.mkdir(exist_ok=True)
    out = INTAKES_DIR / f"{slug}-{record_id}.json"
    out.write_text(
        json.dumps(
            {
                "record_id": record_id,
                "business": business,
                "contact": f.get("Contact First Name", ""),
                "phone": f.get("Phone", ""),
                "call_id": f.get("Call ID", ""),
                "duration_seconds": f.get("Duration (s)", 0),
                "summary": f.get("Summary", ""),
                "recording_url": f.get("Recording URL", ""),
                "structured": structured,
                "transcript": f.get("Transcript", ""),
            },
            indent=2,
        )
    )
    print(out)


def cmd_mark(cfg: dict[str, str], record_id: str, status: str) -> None:
    with _client(cfg) as c:
        resp = c.patch(
            f"/{cfg['table']}/{record_id}",
            json={"fields": {"Status": status}, "typecast": True},
        )
        resp.raise_for_status()
    print(f"{record_id} → Status = {status}")


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] not in ("list", "pull", "mark"):
        sys.exit(__doc__)
    cfg = _load_env()
    if args[0] == "list":
        cmd_list(cfg)
    elif args[0] == "pull":
        if len(args) != 2:
            sys.exit("usage: fetch_intakes.py pull <record_id>")
        cmd_pull(cfg, args[1])
    else:
        if len(args) != 3:
            sys.exit('usage: fetch_intakes.py mark <record_id> "<status>"')
        cmd_mark(cfg, args[1], args[2])


if __name__ == "__main__":
    main()
