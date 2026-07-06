#!/usr/bin/env python3
"""Create the Assessments table in an existing Airtable base.

Run once, after you've created an empty base in the Airtable UI (the guide's
"Airtable base (5 min)" step). This adds the Assessments table with the exact
fields app.py writes to, so you don't have to click each field in by hand.

Requires a token with `schema.bases:write` (in addition to data.records:write).

    AIRTABLE_TOKEN=pat... AIRTABLE_BASE_ID=app... python setup_airtable.py
"""
import os
import sys
import urllib.request
import json

TOKEN = os.environ["AIRTABLE_TOKEN"]
BASE = os.environ["AIRTABLE_BASE_ID"]
TABLE = os.environ.get("AIRTABLE_TABLE", "Assessments")

fields = [
    {"name": "Business Name", "type": "singleLineText"},
    {"name": "Contact First Name", "type": "singleLineText"},
    {"name": "Phone", "type": "singleLineText"},
    {"name": "Call ID", "type": "singleLineText"},
    {"name": "Duration (s)", "type": "number", "options": {"precision": 0}},
    {"name": "Ended Reason", "type": "singleLineText"},
    {"name": "Transcript", "type": "multilineText"},
    {"name": "Summary", "type": "multilineText"},
    {"name": "Recording URL", "type": "url"},
    {"name": "Structured Data", "type": "multilineText"},
    {
        "name": "Status",
        "type": "singleSelect",
        "options": {
            "choices": [
                {"name": "New"},
                {"name": "Deck Generating"},
                {"name": "Deck Ready"},
                {"name": "Sent"},
                {"name": "Won"},
                {"name": "Lost"},
            ]
        },
    },
]

body = json.dumps({"name": TABLE, "fields": fields}).encode()
req = urllib.request.Request(
    f"https://api.airtable.com/v0/meta/bases/{BASE}/tables",
    data=body,
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
    method="POST",
)
try:
    with urllib.request.urlopen(req) as resp:
        out = json.load(resp)
    print(f"✅ Created table {TABLE!r} (id={out.get('id')}) with {len(fields)} fields")
except urllib.error.HTTPError as e:
    detail = e.read().decode()
    if "DUPLICATE_TABLE_NAME" in detail or "already exists" in detail:
        print(f"ℹ️  Table {TABLE!r} already exists — nothing to do.")
        sys.exit(0)
    print(f"❌ {e.code}: {detail}", file=sys.stderr)
    sys.exit(1)
