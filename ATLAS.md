# ATLAS.md

> This file is maintained by Claude Code and read by Atlas (your AI Chief of Staff).
> You don't need to edit it manually — Claude Code updates it at the end of each work session.

## Meta

| Field | Value |
|-------|-------|
| **Project** | Carolina Redesign |
| **One-liner** | Columbia SC editorial site + AI Opportunity Assessment service (Vapi intake → webhook → HyperAgent report) |
| **Status** | building |
| **Last Active** | 2026-07-06 |
| **Stall Threshold** | 7 days |
| **Repo** | https://github.com/jimmyardis/carolina-redesign |
| **Stack** | Static HTML/CSS, GitHub Pages |

## Current State

AI Opportunity Assessment pipeline upgraded to the v2.1 directive set (2026-07-06): directives now live in `directives/` (intake script v2.1, generation spec v2.1, opportunity taxonomy v1.1), the canonical interactive report template is at `templates/assessment_interactive.html` with all spec-§7 changes applied (readiness scorecard, path badges, tool alternatives, L6 strip, build risk/metric lines, safe-use card), and the live Vapi assistant was PATCHed to the v2.1 script — persona renamed Caroline → Reese per directive, consent-first opening, 11 gate probes, nested §8 extraction schema. Webhook parser handles both old and new schema shapes. Editorial site (Federalism Papers etc.) unchanged and live via GitHub Pages.

## Next Action

Redeploy `intake-webhook/` to Railway (if it's live there) so the nested-schema parsing is in production, then run one test call against the Reese assistant end to end.

## Blockers

- None

## Open Questions

- Persona rename Caroline → Reese was applied per the v2.1 directive — confirm the name, and update the ElevenLabs voice when the real voice ID is chosen (currently vapi "Emma").
- Is the intake-webhook deployed on Railway yet? README setup steps (Airtable base, HyperAgent webhook URL) may still be pending.
- Target publication cadence for The Federalism Papers series?

## Session Log

<!-- Append-only. Most recent session on top. Claude Code adds an entry at the end of each work session. -->

### 2026-07-06

- Imported the v2.1 directive set (authored in Claude online) into `directives/`: `intake_script_v2.md` (v2.1), `generation_spec_v2.md` (v2.1), `opportunity_taxonomy.md` (v1.1)
- Established `templates/assessment_interactive.html` as the canonical report template (from the Tidewater sample) and applied the full generation-spec §7 work list: new "Where you stand" readiness-scorecard section (six bars + stage chip + verbatim disclaimer), quick-win path badges (DIY / Guided DIY) + "Also fits" alternative lines, help strip replaced with drop-in L6 verbatim, build cards gained path badges + "Worth knowing" / "It worked if" lines, safe-use starter card between Impact and Paths, extended data arrays with placeholder content, footer version comment `template v2.1 · taxonomy v1.1 · intake v2.1 · spec v2.1`. Also added a scan-signals strip in the why-section (spec §3.2 requires it as an editable copy block though §7 omitted it). Verified headless: zero JS errors, all new elements render, scorecard bars animate
- Rewrote `caroline_build.py` to intake script v2.1 and PATCHed the live Vapi assistant (HTTP 200): consent-first opening, blocks A–E with the four new gate probes, implementation-preference question, nested §8 structured-data schema. Decision: persona renamed Caroline → Reese because the directive names Reese explicitly; name is a single `AGENT_NAME` constant — one-word change + re-run to revert
- Updated `intake-webhook/app.py` to read business/contact from the nested `profile` object with legacy flat-schema fallbacks; verified both shapes parse. Not redeployed to Railway this session
- Left mid-stream: voice is still vapi "Emma" pending a real ElevenLabs voice ID; webhook redeploy + end-to-end test call still to do

### 2026-05-23

- Created ATLAS.md for project tracking
- No code changes this session — file placement only
