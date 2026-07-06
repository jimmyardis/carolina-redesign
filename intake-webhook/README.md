# Carolina Redesign — Intake Webhook

Replaces the Make.com scenario from the HyperAgent guide. One small FastAPI
service that receives Vapi's end-of-call POST and fans out to three branches:

1. **Airtable** — create a record (client data, transcript, structured data, status)
2. **Assessment Builder (HTTP)** — POST transcript + structured data to the HyperAgent
   webhook so the deck auto-generates
3. **Telegram** — ping you: "New intake from <Business> — deck generating"

No Make.com subscription, no visual canvas. You own the whole thing.

## Data flow

```
Caroline (Vapi)  --end-of-call-report-->  /vapi-webhook
                                              │  (filter: ignore non-end-of-call events)
                                              │  (parse: pull business, transcript, structuredData)
                                              ├──► Airtable  Create Record   (Status = Deck Generating)
                                              ├──► Assessment Builder  POST { <body_key>: prompt }
                                              └──► Telegram  sendMessage
```

## What still needs YOU (external UIs — can't be automated)

1. **Airtable base** — create an empty base named "Carolina Redesign Pipeline" in the
   Airtable UI, grab its Base ID (`app...`). Create a token at
   https://airtable.com/create/tokens with scopes `data.records:write` +
   `schema.bases:write`. Then run once:

   ```bash
   AIRTABLE_TOKEN=pat... AIRTABLE_BASE_ID=app... python setup_airtable.py
   ```

   That builds the `Assessments` table with all the right fields automatically.

2. **Assessment Builder webhook** — in HyperAgent, on the Assessment Builder agent →
   Invocations tab → enable Webhook/API → copy the **URL**, **auth token**, and note
   the **example request body key** (`message` vs `prompt`). Put those in the env vars
   below. Set `ASSESSMENT_BUILDER_BODY_KEY` to match exactly.

## Environment variables

See `.env.example`. On Railway, set them in the service Variables tab.

## Local run

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
# smoke test:
curl -X POST localhost:8000/vapi-webhook -H 'Content-Type: application/json' --data @sample_end_of_call.json
```

`GET /health` reports which branches are configured.

## Deploy (Railway)

- Root directory: `intake-webhook`
- Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
- Set all env vars from `.env.example`.

## Wire Caroline to it

Set Caroline's `serverUrl` to `https://<railway-domain>/vapi-webhook` — either in the
Vapi dashboard, or via the Vapi API (extend `../caroline_build.py`). If you set
`VAPI_WEBHOOK_SECRET`, configure the same value as Caroline's server secret so the
service can reject spoofed calls.
