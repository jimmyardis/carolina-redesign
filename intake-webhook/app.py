#!/usr/bin/env python3
"""Carolina Redesign — intake webhook.

Replaces the Make.com scenario. Receives Vapi's end-of-call POST, then fans out
to three destinations exactly like the original guide's Router:

  1. Airtable  — create a record (client data, transcript, structured data, status)
  2. HTTP      — POST transcript + structured data to the Assessment Builder webhook
                 (HyperAgent) so the deck auto-generates
  3. Telegram  — ping you: "New intake from <Business> — deck generating"

Everything is configured via environment variables (see .env.example). The service
verifies Vapi's payload is an `end-of-call-report` before doing anything, so other
Vapi events (status-update, transcript, etc.) are ignored — that's the "Filter"
module from the guide.

Run locally:  uvicorn app:app --host 0.0.0.0 --port 8000
On Railway:   start command = `uvicorn app:app --host 0.0.0.0 --port $PORT`
"""
from __future__ import annotations

import json
import logging
import os
from typing import Any

import httpx
from fastapi import FastAPI, Header, HTTPException, Request

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("intake")

app = FastAPI(title="Carolina Redesign Intake Webhook")

# ---------------------------------------------------------------------------
# Config (all via env)
# ---------------------------------------------------------------------------
# Optional shared secret: Vapi can send a custom header on the server URL. If set,
# we reject any request that doesn't present it. Configure the same value in Vapi's
# assistant serverUrl secret / header.
VAPI_WEBHOOK_SECRET = os.getenv("VAPI_WEBHOOK_SECRET", "").strip()

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN", "").strip()
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID", "").strip()
AIRTABLE_TABLE = os.getenv("AIRTABLE_TABLE", "Assessments").strip()

ASSESSMENT_BUILDER_URL = os.getenv("ASSESSMENT_BUILDER_URL", "").strip()
ASSESSMENT_BUILDER_TOKEN = os.getenv("ASSESSMENT_BUILDER_TOKEN", "").strip()
# HyperAgent authenticates webhook calls with a custom header, not Bearer auth.
# The endpoint's 401 body names it: X-Hyperagent-Webhook-Secret.
ASSESSMENT_BUILDER_AUTH_HEADER = os.getenv(
    "ASSESSMENT_BUILDER_AUTH_HEADER", "X-Hyperagent-Webhook-Secret"
).strip()
# HyperAgent receives any POSTed JSON as the user message; we send the intake under
# this key. "message" is human-readable; change only if your endpoint expects another.
ASSESSMENT_BUILDER_BODY_KEY = os.getenv("ASSESSMENT_BUILDER_BODY_KEY", "message").strip()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()


# ---------------------------------------------------------------------------
# Payload parsing — normalize Vapi's end-of-call-report into a flat dict
# ---------------------------------------------------------------------------
def parse_end_of_call(message: dict[str, Any]) -> dict[str, Any]:
    """Pull the fields we care about out of Vapi's `message` object.

    Vapi nests things a bit; structured-data extraction lands under
    message.analysis.structuredData. We defend against missing keys throughout
    because call reports vary (voicemail, hangups, short calls).
    """
    analysis = message.get("analysis") or {}
    structured = analysis.get("structuredData") or {}
    customer = message.get("customer") or {}
    call = message.get("call") or {}

    # Business name / contact name: intake script v2.1 nests them under `profile`;
    # older flat-schema calls may still arrive, so keep the legacy fallbacks.
    profile = structured.get("profile") or {}
    business = (
        profile.get("business")
        or structured.get("business_name")
        or structured.get("businessName")
        or structured.get("company")
        or ""
    )
    contact = (
        profile.get("name")
        or structured.get("contact_first_name")
        or structured.get("first_name")
        or structured.get("name")
        or ""
    )

    return {
        "business": business.strip() if isinstance(business, str) else business,
        "contact": contact.strip() if isinstance(contact, str) else contact,
        "phone": customer.get("number", ""),
        "call_id": message.get("call", {}).get("id") or call.get("id", ""),
        "ended_reason": message.get("endedReason", ""),
        "duration_seconds": message.get("durationSeconds")
        or message.get("duration")
        or 0,
        "transcript": message.get("transcript", ""),
        "summary": message.get("summary") or analysis.get("summary", ""),
        "recording_url": message.get("recordingUrl")
        or message.get("stereoRecordingUrl", ""),
        "structured": structured,
    }


# ---------------------------------------------------------------------------
# Branch 1 — Airtable: Create Record
# ---------------------------------------------------------------------------
async def write_airtable(client: httpx.AsyncClient, data: dict[str, Any]) -> dict:
    if not (AIRTABLE_TOKEN and AIRTABLE_BASE_ID):
        return {"skipped": "airtable not configured"}

    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE}"
    fields = {
        "Business Name": data["business"] or "Unknown",
        "Contact First Name": data["contact"],
        "Phone": data["phone"],
        "Call ID": data["call_id"],
        "Duration (s)": data["duration_seconds"],
        "Ended Reason": data["ended_reason"],
        "Transcript": data["transcript"],
        "Summary": data["summary"],
        "Recording URL": data["recording_url"],
        "Structured Data": json.dumps(data["structured"], indent=2),
        "Status": "Deck Generating",
    }
    # Drop empties so Airtable doesn't choke on unknown/blank typed fields.
    fields = {k: v for k, v in fields.items() if v not in ("", None)}

    resp = await client.post(
        url,
        headers={
            "Authorization": f"Bearer {AIRTABLE_TOKEN}",
            "Content-Type": "application/json",
        },
        json={"fields": fields, "typecast": True},
    )
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Branch 2 — HTTP: POST to the Assessment Builder (HyperAgent) webhook
# ---------------------------------------------------------------------------
async def trigger_assessment_builder(
    client: httpx.AsyncClient, data: dict[str, Any]
) -> dict:
    if not ASSESSMENT_BUILDER_URL:
        return {"skipped": "assessment builder not configured"}

    # Compose the prompt the builder agent receives. It gets the full transcript
    # plus the structured extraction so the deck generation has everything.
    prompt = (
        f"New AI Opportunity Assessment intake.\n\n"
        f"Business: {data['business'] or 'Unknown'}\n"
        f"Contact: {data['contact']}\n"
        f"Phone: {data['phone']}\n\n"
        f"--- STRUCTURED DATA ---\n"
        f"{json.dumps(data['structured'], indent=2)}\n\n"
        f"--- FULL TRANSCRIPT ---\n"
        f"{data['transcript']}"
    )
    body = {ASSESSMENT_BUILDER_BODY_KEY: prompt}

    headers = {"Content-Type": "application/json"}
    if ASSESSMENT_BUILDER_TOKEN:
        headers[ASSESSMENT_BUILDER_AUTH_HEADER] = ASSESSMENT_BUILDER_TOKEN

    resp = await client.post(ASSESSMENT_BUILDER_URL, headers=headers, json=body)
    resp.raise_for_status()
    # Builder may return JSON or plain text; handle both.
    try:
        return resp.json()
    except Exception:
        return {"status_code": resp.status_code, "text": resp.text[:500]}


# ---------------------------------------------------------------------------
# Branch 3 — Telegram: notify
# ---------------------------------------------------------------------------
async def notify_telegram(client: httpx.AsyncClient, data: dict[str, Any]) -> dict:
    if not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID):
        return {"skipped": "telegram not configured"}

    business = data["business"] or "Unknown business"
    text = (
        f"📞 New intake from *{business}*\n"
        f"Contact: {data['contact'] or 'n/a'} ({data['phone'] or 'no number'})\n"
        f"Duration: {data['duration_seconds']}s — deck generating…"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    resp = await client.post(
        url,
        json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"},
    )
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/health")
async def health() -> dict:
    return {
        "ok": True,
        "airtable": bool(AIRTABLE_TOKEN and AIRTABLE_BASE_ID),
        "assessment_builder": bool(ASSESSMENT_BUILDER_URL),
        "telegram": bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID),
    }


@app.post("/vapi-webhook")
async def vapi_webhook(
    request: Request,
    x_vapi_secret: str | None = Header(default=None),
) -> dict:
    # Optional auth gate
    if VAPI_WEBHOOK_SECRET and x_vapi_secret != VAPI_WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="bad secret")

    payload = await request.json()
    message = payload.get("message") or {}
    msg_type = message.get("type", "")

    # --- Filter module: only act on end-of-call-report ---
    if msg_type != "end-of-call-report":
        log.info("ignoring vapi event: %s", msg_type or "(none)")
        return {"ignored": msg_type or "no-type"}

    data = parse_end_of_call(message)
    log.info("end-of-call for business=%r phone=%r", data["business"], data["phone"])

    results: dict[str, Any] = {}
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Router: three branches. Run independently; one failing shouldn't
        # sink the others (a Telegram outage must not lose the Airtable row).
        for name, coro in (
            ("airtable", write_airtable(client, data)),
            ("assessment_builder", trigger_assessment_builder(client, data)),
            ("telegram", notify_telegram(client, data)),
        ):
            try:
                results[name] = await coro
            except Exception as e:  # noqa: BLE001 — log and continue per branch
                log.exception("branch %s failed", name)
                results[name] = {"error": str(e)}

    return {"processed": True, "business": data["business"], "results": results}
