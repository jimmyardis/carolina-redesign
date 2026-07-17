# ATLAS.md

> This file is maintained by Claude Code and read by Atlas (your AI Chief of Staff).
> You don't need to edit it manually — Claude Code updates it at the end of each work session.

## Meta

| Field | Value |
|-------|-------|
| **Project** | Carolina Redesign |
| **One-liner** | Columbia SC editorial site + AI Opportunity Assessment service (Vapi intake → webhook → Airtable queue → Claude Code report) |
| **Status** | building |
| **Last Active** | 2026-07-16 |
| **Stall Threshold** | 7 days |
| **Repo** | https://github.com/jimmyardis/carolina-redesign |
| **Stack** | Static HTML/CSS, GitHub Pages |

## Current State

HyperAgent is out of the pipeline (2026-07-16): the always-on Railway webhook (`carolina-intake`, live) queues each Vapi intake in Airtable and now **auto-drafts the report via the Claude API** — `intake-webhook/report_gen.py` runs Claude Opus 4.8 with web search against the v2.1 spec/taxonomy/frozen template (deploy-time copies in `intake-webhook/assets/`, synced by `sync_assets.sh`), attaches the draft HTML to the Airtable row (`Draft Report` field), sets Status "Draft Ready", and Telegrams. User reviews/edits before emailing. `/build-assessment` Claude Code skill is the manual fallback. Deployed with `report_gen: true`; stub tests + API-shape sanity check pass; full paid end-to-end draft not yet run.

## Next Action

Run one full end-to-end draft on the sample intake (~$2–4 API cost, user go-ahead needed), then a real test call against Reese.

## Blockers

- None — Airtable token fixed same day (all four scopes on `cr_pipeline`; watch out: `data.recordComments:read` masquerades as `data.records:read` in the scope picker), `Draft Report` attachment field created (`fldnY7j0dIMHRTBET`).

## Open Questions

- Persona rename Caroline → Reese was applied per the v2.1 directive — confirm the name, and update the ElevenLabs voice when the real voice ID is chosen (currently vapi "Emma").
- Target publication cadence for The Federalism Papers series?

## Session Log

<!-- Append-only. Most recent session on top. Claude Code adds an entry at the end of each work session. -->

### 2026-07-16

- Took HyperAgent out of the loop (user ran out of credits). Decision: keep the Railway webhook as the always-on catcher (that was HyperAgent's only real advantage) and move report generation to Claude Code, run on demand from the user's machine — no per-report subscription, human review before delivery
- Rewrote `intake-webhook/app.py`: removed the Assessment Builder branch entirely; Airtable Status is now "Ready for Report" (Airtable = the report queue); Telegram message points at `/build-assessment`; added a one-retry guard on the Telegram POST after a transient `httpx.ReadTimeout` from Railway
- New `intake-webhook/fetch_intakes.py` — local queue helper (`list` / `pull <rec>` / `mark <rec> <status>`), reads Airtable creds from `~/.env` (copied there from the Railway service this session)
- New repo skill `.claude/skills/build-assessment/SKILL.md` — the Claude Code replacement for the HyperAgent Assessment Builder; same governing documents (generation spec v2.1 §2–§5, taxonomy v1.1, frozen template v2.1), same run shape (pull → fresh scan → gate → populate arrays → 13-check QA → mark done), run notes per client
- Deleted the four `ASSESSMENT_BUILDER_*` vars from the `carolina-intake` Railway service, deployed twice (both SUCCESS), verified end to end with the sample payload: Airtable row created with correct status + Telegram ping delivered; test rows deleted afterwards
- `.gitignore` now excludes `intakes/` and `clients/` — client transcripts/reports must never reach the public Pages repo
- Blocker found: the Airtable token is write-only (per the original least-privilege setup), so `fetch_intakes.py list` gets 403 — user must add `data.records:read` at airtable.com/create/tokens and update the value in `~/.env` + Railway
- **Second pass same day — auto-draft via Claude API** (user decision: first draft automatic, human review before delivery). New `intake-webhook/report_gen.py`: background task after the Airtable write runs Claude Opus 4.8 (adaptive thinking, effort high, `web_search_20260209` + `web_fetch_20260209`, streaming, `pause_turn` continuation loop, prompt-cached template prefix) with the spec/taxonomy/template as system context; extracts the HTML document; uploads it as an Airtable attachment via `content.airtable.com` uploadAttachment; Status "Drafting" → "Draft Ready"; Telegram pings on success/failure; any failure reverts to "Ready for Report" so `/build-assessment` remains the fallback
- Assets copied to `intake-webhook/assets/` via new `sync_assets.sh` (Railway root is intake-webhook, can't read ../directives) — re-sync + redeploy after directive/template changes
- Stub tests pass (extract_html, endpoint schedules background job with fake record); one tiny real API call verified the key + request shape (Opus 4.8 accepted, ~$0.03); `ANTHROPIC_API_KEY` set on Railway; deployed SUCCESS, `/health` shows `report_gen: true`, model claude-opus-4-8
- NOT yet done: `Draft Report` attachment field in Airtable (needs schema-scope token or manual UI add); full paid end-to-end draft (~$2–4) awaiting user go-ahead
- Left mid-stream: no real end-to-end call on v2.1 yet; voice still vapi "Emma"; repo still not pushed (public Pages repo publishes directives + the new skill)

### 2026-07-06

- Imported the v2.1 directive set (authored in Claude online) into `directives/`: `intake_script_v2.md` (v2.1), `generation_spec_v2.md` (v2.1), `opportunity_taxonomy.md` (v1.1)
- Established `templates/assessment_interactive.html` as the canonical report template (from the Tidewater sample) and applied the full generation-spec §7 work list: new "Where you stand" readiness-scorecard section (six bars + stage chip + verbatim disclaimer), quick-win path badges (DIY / Guided DIY) + "Also fits" alternative lines, help strip replaced with drop-in L6 verbatim, build cards gained path badges + "Worth knowing" / "It worked if" lines, safe-use starter card between Impact and Paths, extended data arrays with placeholder content, footer version comment `template v2.1 · taxonomy v1.1 · intake v2.1 · spec v2.1`. Also added a scan-signals strip in the why-section (spec §3.2 requires it as an editable copy block though §7 omitted it). Verified headless: zero JS errors, all new elements render, scorecard bars animate
- Rewrote `caroline_build.py` to intake script v2.1 and PATCHed the live Vapi assistant (HTTP 200): consent-first opening, blocks A–E with the four new gate probes, implementation-preference question, nested §8 structured-data schema. Decision: persona renamed Caroline → Reese because the directive names Reese explicitly; name is a single `AGENT_NAME` constant — one-word change + re-run to revert
- Updated `intake-webhook/app.py` to read business/contact from the nested `profile` object with legacy flat-schema fallbacks; verified both shapes parse. Not redeployed to Railway this session
- Redeployed intake-webhook to Railway (`carolina-intake` project, deployment SUCCESS, health green); confirmed the Vapi assistant's serverUrl already points at it and the shared secret is enforced
- Drafted `HYPERAGENT_HANDOFF_v2.1.md` (also copied to Windows Downloads) — the migration message for the HyperAgent Assessment Builder agent
- Left mid-stream: HyperAgent agent still runs v1 instructions until the handoff is pasted in; voice is still vapi "Emma" pending a real ElevenLabs voice ID; end-to-end test call still to do; repo not pushed (public Pages repo would publish the directives — private-repo option offered)

### 2026-05-23

- Created ATLAS.md for project tracking
- No code changes this session — file placement only
