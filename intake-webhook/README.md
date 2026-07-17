# Carolina Redesign — Intake Webhook

Always-on intake catcher **and first-draft generator** (Railway service
`carolina-intake`). One FastAPI service that receives Vapi's end-of-call POST,
queues the intake, then auto-drafts the report with the Claude API:

1. **Airtable** — create a record (client data, transcript, structured data,
   Status = `Ready for Report`). Airtable is the report queue.
2. **Telegram** — ping you: "New intake from <Business> — queued in Airtable."
3. **Auto-draft** (`report_gen.py`, background task) — Claude Opus 4.8 with web
   search follows `assets/generation_spec_v2.md` + taxonomy + frozen template
   and produces the report HTML; it's attached to the Airtable row (`Draft
   Report` field), Status → `Draft Ready`, Telegram pings again. You review and
   edit the draft before emailing it. The old HyperAgent "Assessment Builder"
   was retired 2026-07-16.

If `ANTHROPIC_API_KEY` is unset or generation fails, the row stays at
`Ready for Report` and the **`/build-assessment`** Claude Code skill
(`.claude/skills/build-assessment/`) is the manual path.

## Data flow

```
Reese (Vapi)  --end-of-call-report-->  /vapi-webhook   (Railway, always on)
                                           │  (filter + parse)
                                           ├──► Airtable  Create Record   (Status = Ready for Report)
                                           ├──► Telegram  "queued — drafting report"
                                           └──► background: report_gen.py
                                                    Claude Opus 4.8 + web search
                                                    per assets/{spec,taxonomy,template}
                                                    ├─ ok  → attach draft to row, Status = Draft Ready, Telegram ping
                                                    └─ fail→ Status stays Ready for Report, Telegram error
                                                            (fallback: /build-assessment locally)
```

## Assets

`assets/` holds deploy-time copies of the governing documents (the Railway root
dir is `intake-webhook`, so the service can't read `../directives`). After any
directive or template change: `./sync_assets.sh && railway up --detach`.

## Queue helper

```bash
# names of pending intakes
python fetch_intakes.py list
# save one intake (structured data + transcript) to a local JSON file
python fetch_intakes.py pull recXXXXXXXXXXXXXX
# update its status after the report is built / sent
python fetch_intakes.py mark recXXXXXXXXXXXXXX "Report Ready"
```

Reads `AIRTABLE_TOKEN` / `AIRTABLE_BASE_ID` / `AIRTABLE_TABLE` from the environment
or `~/.env`.

## Environment variables

See `.env.example`. On Railway, set them in the service Variables tab.
Auto-draft additionally uses `ANTHROPIC_API_KEY` (required to enable),
`REPORT_MODEL` (default `claude-opus-4-8`), and `AIRTABLE_DRAFT_FIELD`
(default `Draft Report` — must exist as an **attachment** field on the
Assessments table).

## Local run

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
# smoke test:
curl -X POST localhost:8000/vapi-webhook -H 'Content-Type: application/json' --data @sample_end_of_call.json
```

`GET /health` reports which branches are configured.

## Deploy (Railway)

- Project `carolina-intake`, service `carolina-intake`
  (https://carolina-intake-production.up.railway.app)
- Root directory: `intake-webhook`
- Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
- Deploy from this directory: `railway up --detach` (link with
  `railway link --project carolina-intake` first if needed).

## Wire Reese to it

Reese's `serverUrl` points at `https://carolina-intake-production.up.railway.app/vapi-webhook`
— set in the Vapi dashboard or via `../caroline_build.py`. `VAPI_WEBHOOK_SECRET` is
set on the service; Reese sends the same value in `x-vapi-secret` so spoofed calls
are rejected.
