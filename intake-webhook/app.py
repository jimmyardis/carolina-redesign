#!/usr/bin/env python3
"""Carolina Redesign — intake webhook.

Always-on intake catcher. Receives Vapi's end-of-call POST and fans out to two
destinations:

  1. Airtable  — create a record (client data, transcript, structured data,
                 Status = "Ready for Report"). Airtable is the report queue.
  2. Telegram  — ping you: "New intake from <Business> — queued for report"

Then, if ANTHROPIC_API_KEY is set, a background task (report_gen.py) drafts the
report with Claude Opus 4.8 and attaches it to the Airtable row for review —
the Claude API replacement for the retired HyperAgent Assessment Builder
(2026-07-16). If generation is disabled or fails, the row stays queued and the
/build-assessment Claude Code skill is the manual path.

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
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Request

import report_gen

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
        "Status": "Ready for Report",
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
# Branch 2 — Telegram: notify
# ---------------------------------------------------------------------------
async def notify_telegram(client: httpx.AsyncClient, data: dict[str, Any]) -> dict:
    if not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID):
        return {"skipped": "telegram not configured"}

    business = data["business"] or "Unknown business"
    if report_gen.enabled():
        followup = "Drafting the report now — expect a 'draft ready' ping."
    else:
        followup = "Run /build-assessment in carolina-redesign to generate the report."
    text = (
        f"📞 New intake from *{business}*\n"
        f"Contact: {data['contact'] or 'n/a'} ({data['phone'] or 'no number'})\n"
        f"Duration: {data['duration_seconds']}s — queued in Airtable.\n"
        f"{followup}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    # Telegram occasionally times out from Railway; one retry keeps the ping
    # without risking the webhook response (Airtable already has the row).
    last_exc: Exception | None = None
    for _ in range(2):
        try:
            resp = await client.post(
                url,
                json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"},
            )
            resp.raise_for_status()
            return resp.json()
        except (httpx.TimeoutException, httpx.TransportError) as e:
            last_exc = e
    raise last_exc  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/health")
async def health() -> dict:
    return {
        "ok": True,
        "airtable": bool(AIRTABLE_TOKEN and AIRTABLE_BASE_ID),
        "telegram": bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID),
        "report_gen": report_gen.enabled(),
        "report_model": report_gen.REPORT_MODEL if report_gen.enabled() else None,
    }


@app.post("/vapi-webhook")
async def vapi_webhook(
    request: Request,
    background: BackgroundTasks,
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
        # Router: two branches. Run independently; one failing shouldn't
        # sink the other (a Telegram outage must not lose the Airtable row).
        for name, coro in (
            ("airtable", write_airtable(client, data)),
            ("telegram", notify_telegram(client, data)),
        ):
            try:
                results[name] = await coro
            except Exception as e:  # noqa: BLE001 — log and continue per branch
                log.exception("branch %s failed", name)
                results[name] = {"error": str(e)}

    # Auto-draft: runs after this response returns, so Vapi isn't kept waiting.
    record_id = (results.get("airtable") or {}).get("id")
    if report_gen.enabled() and record_id:
        background.add_task(report_gen.run_report_job, data, record_id)
        results["report_gen"] = {"scheduled": True, "record": record_id}
    elif report_gen.enabled():
        results["report_gen"] = {"skipped": "no airtable record to attach draft to"}
    else:
        results["report_gen"] = {"skipped": "ANTHROPIC_API_KEY not configured"}

    return {"processed": True, "business": data["business"], "results": results}
