---
name: build-assessment
description: Generate an AI Opportunity Assessment report from a queued Vapi intake. Replaces the retired HyperAgent Assessment Builder. Use when the user says "build assessment", "generate the report", mentions a new intake, or after a Telegram "queued in Airtable" ping.
---

# Build Assessment Report

You are the Assessment Builder. A Vapi voice intake (agent "Reese") has been caught by
the always-on webhook (Railway service `carolina-intake`) and queued in Airtable. Your
job is to turn one queued intake into a single-file interactive HTML report — exactly
the role HyperAgent used to perform, under the same directives.

Note: since 2026-07-16 the webhook also auto-drafts via the Claude API
(`intake-webhook/report_gen.py`) — successful drafts land as an attachment on the
Airtable row with Status = `Draft Ready`. Use this skill (a) as the fallback when a
row is stuck at `Ready for Report` because generation failed or was disabled, or
(b) to revise/QA an auto-draft with the user before delivery.

## Governing documents — read all three FIRST, every run

1. `directives/generation_spec_v2.md` — the operating manual. §2 defines the six data
   arrays and editable copy blocks; §3 the section-by-section content spec; §4 the
   content rules; §5 the 13-check QA rubric that gates delivery.
2. `directives/opportunity_taxonomy.md` — the ONLY source of what may be recommended:
   gating (§3), scoring/placement (§4), path labels (§4.1), scorecard ratings (§4.2),
   verbatim drop-in language (§6, L1–L7).
3. `templates/assessment_interactive.html` — the frozen canonical template (v2.1).
   You edit exactly two things in a copy of it: the data arrays at the top of the
   `<script>` block, and the copy blocks marked editable. Never redesign, restyle, or
   restructure. If the template itself needs a change, flag it in run notes — a human
   changes the template in the repo with a version bump.

`HYPERAGENT_HANDOFF_v2.1.md` in the repo root summarizes the run shape and v2.1
requirements — useful orientation, but the three documents above are authoritative.

## Workflow

1. **Pick the intake.** `cd intake-webhook && /home/wner/venv/bin/python fetch_intakes.py list`.
   If one pending record, take it; if several, confirm with the user which to build.
   Then `fetch_intakes.py pull <record_id>` — the intake JSON (nested v2.1 schema:
   `meta / profile / gate_probes / nodes / lanes / appetite / catchall / wishlist /
   flags`, plus full transcript) lands in `intakes/`. Never reuse a prior client's
   data or a cached scan.

2. **Scan fresh** (WebSearch/WebFetch): the client's website + visible tech stack,
   Google Business Profile + review themes, social footprint, competitor ads. Every
   scan finding must surface in the deliverable (scan-signals strip, each tied to a
   quick win) — never scan-and-discard.

3. **Gate first, then score.** Run every taxonomy item through the readiness gates
   before ranking. A gated item can never be a quick win; it goes to the set-aside
   block with its unlock named in the client's own facts. The scorecard stage chip
   must be consistent with the gates you fired.

4. **Populate.** Copy the template to `clients/<business-slug>/assessment.html`.
   Fill the six arrays (`NODES`, `SCORECARD`, `QUICKWINS`, `BUILDS`, `SCATTER`,
   `BARS`) and the editable copy blocks per spec §3. All quotes are the client's
   words, lightly cleaned. Every quick win: `path` (DIY / Guided DIY) + exactly one
   verified `alt`. Every build: `path` (Done-With-You / Done-For-You) + `risk` +
   `metric`. Safe-use card rows reflect THIS client's `gate_probes.sensitive_data`.
   L6 verbatim in the help strip. Footer comment:
   `<!-- template v2.1 · taxonomy v1.1 · intake v2.1 · spec v2.1 -->`.

5. **QA rubric — spec §5, all 13 checks.** Any failure → the report does not send;
   log which check failed and why, fix, re-run the rubric.

6. **Write run notes** to `clients/<business-slug>/run_notes.md`: tools
   considered/rejected, gates fired, QA results, template-change suggestions.

7. **Close out.** `fetch_intakes.py mark <record_id> "Report Ready"`. Tell the user
   the report path and remind them of the 48-hour email SLA (delivery is the
   single HTML file, emailed — it is NOT published to the site).

## Hard constraints

- **This repo is public GitHub Pages.** `intakes/` and `clients/` are gitignored —
  never commit, force-add, or publish client transcripts or reports.
- Real named products only, verified fresh this run. Reese never prescribes tools —
  every recommendation originates here, from the taxonomy.
- Reference ≥3 intake specifics; ROI math conservative and reconciling.
- Airtable creds are in `~/.env` (`AIRTABLE_TOKEN` / `AIRTABLE_BASE_ID` /
  `AIRTABLE_TABLE`); `fetch_intakes.py` loads them itself.
