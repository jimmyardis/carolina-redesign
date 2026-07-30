#!/usr/bin/env python3
"""Auto-draft generation — the Claude API replacement for HyperAgent.

After the webhook queues an intake in Airtable, run_report_job() (scheduled as
a FastAPI background task) generates a FIRST DRAFT of the assessment report:

  1. Claude Opus 4.8 (web search enabled) follows the same governing documents
     HyperAgent did — assets/generation_spec_v2.md, assets/opportunity_taxonomy.md,
     assets/assessment_interactive.html — and returns the populated single-file
     HTML report.
  2. The draft is uploaded to the Airtable row as an attachment ("Draft Report"
     field), Status → "Draft Ready", and Telegram pings you.
  3. The user reviews/edits the draft before emailing it (48h SLA). If anything
     fails, Status stays "Ready for Report" and /build-assessment is the fallback.

Requires ANTHROPIC_API_KEY. The three asset files are copies synced from the
repo by sync_assets.sh — re-sync + redeploy after any directive/template change.
"""
from __future__ import annotations

import base64
import json
import logging
import os
from pathlib import Path
from typing import Any

import httpx
from anthropic import AsyncAnthropic

log = logging.getLogger("report_gen")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()
REPORT_MODEL = os.getenv("REPORT_MODEL", "claude-opus-4-8").strip()
DRAFT_FIELD = os.getenv("AIRTABLE_DRAFT_FIELD", "Draft Report").strip()
MAX_CONTINUATIONS = 8

ASSETS = Path(__file__).resolve().parent / "assets"


def enabled() -> bool:
    return bool(ANTHROPIC_API_KEY)


def _load_assets() -> dict[str, str]:
    return {
        "spec": (ASSETS / "generation_spec_v2.md").read_text(),
        "taxonomy": (ASSETS / "opportunity_taxonomy.md").read_text(),
        "template": (ASSETS / "assessment_interactive.html").read_text(),
    }


SYSTEM_ROLE = """\
You are the Assessment Builder for Carolina Redesign. You turn one voice-intake
(structured JSON + transcript) into a single-file interactive HTML report — an
AI Opportunity Assessment for a small business.

Your deliverable is produced by editing exactly two things in the frozen
canonical template you are given: the data arrays at the top of its <script>
block (NODES, SCORECARD, QUICKWINS, BUILDS, SCATTER, BARS), and the copy blocks
marked editable. Never redesign, restyle, or restructure the template.

The three documents below are authoritative, in this order of operation:
1. The generation spec — your operating manual. §2 defines the arrays and
   editable copy blocks; §3 the section-by-section content spec; §4 the content
   rules; §5 the 13-check QA rubric that gates delivery.
2. The opportunity taxonomy — the ONLY source of what may be recommended, how
   items are gated (§3), scored/placed (§4), path-labeled (§4.1), scorecard-
   rated (§4.2), and the verbatim drop-in language (§6, L1–L7).
3. The canonical template (v2.2) — with placeholder data showing exactly what
   each array and copy block should look like when populated.

The shape of the run:
- Scan fresh with web search: the client's website + tech stack, Google
  Business Profile + review themes, social footprint, competitor ads. Every
  scan finding must appear in the deliverable (scan-signals strip, each tied to
  a quick win) — never scan-and-discard. Real named products only, verified
  fresh this run; the voice agent never prescribes tools — every
  recommendation originates with you, from the taxonomy.
- Gate first, then score. A gated item can never be a quick win; it goes to the
  set-aside block with its unlock named in the client's own facts. The
  scorecard stage chip must be consistent with the gates you fired.
- All quotes are the client's words, lightly cleaned. Reference ≥3 intake
  specifics. ROI math conservative and reconciling.
- Run the full §5 QA rubric (all 13 checks) yourself before finalizing; fix any
  failure before you output.
- Footer version comment verbatim:
  <!-- template v2.2 · taxonomy v1.1 · intake v2.1 · spec v2.1 -->

OUTPUT FORMAT — this is machine-parsed: after your scan and reasoning, your
final response text must be the COMPLETE populated HTML document and nothing
else — starting with <!DOCTYPE html> and ending with </html>. No markdown
fences, no commentary before or after.
"""


def build_request_messages(data: dict[str, Any]) -> list[dict[str, Any]]:
    intake = (
        f"New AI Opportunity Assessment intake.\n\n"
        f"Business: {data.get('business') or 'Unknown'}\n"
        f"Contact: {data.get('contact', '')}\n"
        f"Phone: {data.get('phone', '')}\n\n"
        f"--- STRUCTURED DATA (intake v2.1 nested schema) ---\n"
        f"{json.dumps(data.get('structured', {}), indent=2)}\n\n"
        f"--- FULL TRANSCRIPT ---\n"
        f"{data.get('transcript', '')}\n\n"
        f"Produce the report now. Remember: final response text = the complete "
        f"HTML document only."
    )
    return [{"role": "user", "content": intake}]


def extract_html(text: str) -> str:
    """Pull the HTML document out of the final response text."""
    lower = text.lower()
    start = lower.find("<!doctype")
    if start == -1:
        start = lower.find("<html")
    end = lower.rfind("</html>")
    if start == -1 or end == -1 or end < start:
        raise ValueError("no complete HTML document in model output")
    return text[start : end + len("</html>")]


async def generate_draft(data: dict[str, Any]) -> str:
    """Run the generation loop; returns the report HTML."""
    assets = _load_assets()
    system = [
        {"type": "text", "text": SYSTEM_ROLE},
        {"type": "text", "text": f"=== GENERATION SPEC (v2.1) ===\n\n{assets['spec']}"},
        {"type": "text", "text": f"=== OPPORTUNITY TAXONOMY (v1.1) ===\n\n{assets['taxonomy']}"},
        {
            "type": "text",
            "text": f"=== CANONICAL TEMPLATE (v2.2) ===\n\n{assets['template']}",
            # Stable prefix — cached across the pause_turn continuations below.
            "cache_control": {"type": "ephemeral"},
        },
    ]
    tools = [
        {"type": "web_search_20260209", "name": "web_search", "max_uses": 15},
        {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": 10},
    ]
    messages = build_request_messages(data)

    client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    response = None
    for _ in range(MAX_CONTINUATIONS + 1):
        async with client.messages.stream(
            model=REPORT_MODEL,
            max_tokens=64000,
            thinking={"type": "adaptive"},
            output_config={"effort": "high"},
            system=system,
            tools=tools,
            messages=messages,
        ) as stream:
            response = await stream.get_final_message()
        if response.stop_reason != "pause_turn":
            break
        # Server-side tool loop hit its iteration limit — resume where it left off.
        messages = build_request_messages(data) + [
            {"role": "assistant", "content": response.content}
        ]
    if response is None or response.stop_reason == "pause_turn":
        raise RuntimeError("generation did not complete within continuation limit")
    if response.stop_reason == "refusal":
        raise RuntimeError("model refused the request")
    if response.stop_reason == "max_tokens":
        raise RuntimeError("output truncated at max_tokens")

    final_text = "".join(b.text for b in response.content if b.type == "text")
    log.info(
        "generation done: stop=%s in=%s out=%s",
        response.stop_reason,
        response.usage.input_tokens,
        response.usage.output_tokens,
    )
    return extract_html(final_text)


# ---------------------------------------------------------------------------
# Airtable + Telegram plumbing
# ---------------------------------------------------------------------------
def _airtable_cfg() -> dict[str, str]:
    return {
        "token": os.getenv("AIRTABLE_TOKEN", "").strip(),
        "base": os.getenv("AIRTABLE_BASE_ID", "").strip(),
        "table": os.getenv("AIRTABLE_TABLE", "Assessments").strip(),
    }


async def _set_status(client: httpx.AsyncClient, record_id: str, status: str) -> None:
    cfg = _airtable_cfg()
    resp = await client.patch(
        f"https://api.airtable.com/v0/{cfg['base']}/{cfg['table']}/{record_id}",
        headers={"Authorization": f"Bearer {cfg['token']}"},
        json={"fields": {"Status": status}, "typecast": True},
    )
    resp.raise_for_status()


async def _upload_draft(
    client: httpx.AsyncClient, record_id: str, html: str, business: str
) -> None:
    cfg = _airtable_cfg()
    slug = "".join(c if c.isalnum() else "-" for c in business.lower()).strip("-") or "report"
    resp = await client.post(
        f"https://content.airtable.com/v0/{cfg['base']}/{record_id}/{DRAFT_FIELD}/uploadAttachment",
        headers={"Authorization": f"Bearer {cfg['token']}"},
        json={
            "contentType": "text/html",
            "filename": f"assessment-{slug}.html",
            "file": base64.b64encode(html.encode()).decode(),
        },
    )
    resp.raise_for_status()


async def _telegram(client: httpx.AsyncClient, text: str) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not (token and chat):
        return
    try:
        await client.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat, "text": text, "parse_mode": "Markdown"},
        )
    except Exception:  # noqa: BLE001 — a lost ping must not fail the job
        log.exception("telegram notify failed")


async def run_report_job(data: dict[str, Any], record_id: str) -> None:
    """Background task: draft the report and attach it to the Airtable row."""
    business = data.get("business") or "Unknown business"
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            await _set_status(client, record_id, "Drafting")
        except Exception:  # noqa: BLE001
            log.exception("could not set Drafting status (continuing)")
        try:
            html = await generate_draft(data)
        except Exception as e:  # noqa: BLE001
            log.exception("draft generation failed for %s", business)
            try:
                await _set_status(client, record_id, "Ready for Report")
            except Exception:  # noqa: BLE001
                log.exception("status revert failed")
            await _telegram(
                client,
                f"⚠️ Draft generation failed for *{business}*: {e}\n"
                f"Intake is still queued — run /build-assessment manually.",
            )
            return
        try:
            await _upload_draft(client, record_id, html, business)
            await _set_status(client, record_id, "Draft Ready")
            await _telegram(
                client,
                f"📝 Draft ready for *{business}* — attached to the Airtable row "
                f"({DRAFT_FIELD}). Review + edit before sending (48h SLA).",
            )
        except Exception as e:  # noqa: BLE001
            log.exception("draft save failed for %s", business)
            await _telegram(
                client,
                f"⚠️ Draft for *{business}* generated but could not be saved to "
                f"Airtable ({e}). Check the '{DRAFT_FIELD}' attachment field exists, "
                f"then run /build-assessment.",
            )
