# ATLAS.md

> This file is maintained by Claude Code and read by Atlas (your AI Chief of Staff).
> You don't need to edit it manually — Claude Code updates it at the end of each work session.

## Meta

| Field | Value |
|-------|-------|
| **Project** | Carolina Redesign |
| **One-liner** | Columbia SC editorial site + AI Opportunity Assessment service (Vapi intake → webhook → Airtable queue → Claude Code report) |
| **Status** | building |
| **Last Active** | 2026-09-02 |
| **Stall Threshold** | 7 days |
| **Repo** | https://github.com/jimmyardis/carolina-redesign |
| **Stack** | Static HTML/CSS, GitHub Pages |

## Current State

**Palmetto Ledger Issue 4 shipped 2026-09-02**: "Department of Agriculture, FY2025" is live at `/palmetto-ledger/agriculture.html` — the first single-agency study in the series, and the second built on the Comptroller General's spending files. All $42.6M of the Department's FY2025 transactions, split pass-through vs. operational, with a fund lens (All/General/Federal/Restricted/Earmarked) that redraws every chart, and the Section 44 appropriation set beside the actuals.

**Palmetto Ledger Issue 3 shipped 2026-08-25**: "South Carolina FY2025 State Spending, Organized by Function" is live at `/palmetto-ledger/fy2025-spending-by-function/`, with its six data files (five CSVs + `taxonomy.py`) published and linked from the page. Built from the Comptroller General's monthly spending transparency files — a second data source for the series alongside the ZBB/appropriations path.

The assessment is now **publicly sellable end to end**: the redesigned checkout-first sales page at `/assessment/` (live 2026-07-31) → $999 Stripe payment link → `/assessment/start/` post-checkout page → Reese intake line → webhook/Airtable/auto-draft pipeline (unchanged since 07-16: `carolina-intake` Railway webhook queues intakes, `report_gen.py` auto-drafts via Claude Opus 4.8, human reviews before emailing). Page promises 48-hour delivery, a 45-min walkthrough, and a 5-hrs/week-or-refund guarantee. Stripe checkout currently runs on the user's single Stripe account (also hosts Secursion products); a per-brand second account was recommended, decision pending.

## Next Action

Run one real test purchase through the live flow (checkout → redirect → start page → call Reese), which also finally verifies the 2026-07-19 Vapi extraction fix; refund it from the Stripe dashboard afterward (~$2 auto-draft will fire).

## Blockers

- None. (Watch-outs: Airtable's attachment preview doesn't run JS, so drafts look empty there — download + open in a browser. `data.recordComments:read` masquerades as `data.records:read` in the Airtable scope picker.)

## Open Questions

- Persona rename Caroline → Reese was applied per the v2.1 directive — confirm the name, and update the ElevenLabs voice when the real voice ID is chosen (currently vapi "Emma").
- Target publication cadence for The Federalism Papers series?

## Session Log

<!-- Append-only. Most recent session on top. Claude Code adds an entry at the end of each work session. -->

### 2026-09-02

- **Published Palmetto Ledger Issue 4** — "Department of Agriculture, FY2025." Standalone page arrived from `~/Downloads/palmetto-ledger-agriculture.html`; copied to `palmetto-ledger/agriculture.html` (fully self-contained — data inlined as a `DATA` object, no CDN scripts, Google Fonts only).
- Same integration treatment as Issue 3, again without touching its visual identity (it shares Issue 3's Spectral/pine/brass family): pine masthead with a `← The Palmetto Ledger` mark, favicon, meta description, and footer links back to the series and the site root.
- **Renumbered:** the file arrived labelled "No. 2 in a series" — it predates the current numbering. Published as **Issue 4**, and The Match Trap moved **4 → 5**, same precedent as last session.
- Issue 4 card added to `/palmetto-ledger/` (newest first) and the research-index chips updated (Issue 4: Agriculture; Issue 5: Coming soon).
- Card figures computed from the page's own embedded data before publishing: $42.6M recorded spend, 7,389 transactions, 807 payees, 44.4% pass-through. Headless render check: 17 treemap cells, 14 rank rows, 15 aid rows, 12 budget rows, 50 payee rows, fund-lens switching recomputes correctly (Federal = $10.2M / 23.8%), zero console errors.
- Verified live at www.carolinaredesign.com after the Pages build (~45s).
- **Note for the next agency study:** the page's own method block flags that ~$20.7M of appropriated personnel spending never appears in the transaction files, and that mapping transactions to program areas needs the Department's internal cost-center structure. Same limits will hit every single-agency issue.

### 2026-08-25

- **Published Palmetto Ledger Issue 3** — "South Carolina FY2025 State Spending, Organized by Function." Source folder came in from `~/Downloads/palmetto-ledger-repo/ledger-repo/`; copied to `palmetto-ledger/fy2025-spending-by-function/` (self-contained `index.html` + `data/`).
- Wired it into the series without touching its own visual identity (it uses its own Spectral/indigo palette, not the Playfair/gold ledger theme): masthead mark and footer now link back to `/palmetto-ledger/`, favicon and meta description added, and a "The data behind this page" block links all six data files — they shipped with the page but nothing referenced them.
- Added the Issue 3 card to `/palmetto-ledger/` (newest first) and updated the research-index chips. **The Match Trap renumbered 3 → 4** so the published issues stay sequential.
- Broadened the ledger method note: it claimed every figure came from the appropriations acts via the ZBB Suite, which isn't true of this issue. It now names the Comptroller General spending files as the second source. The hero blurb still describes only the ZBB path — worth revisiting if more expenditure-data issues follow.
- Headline figures checked against the shipped CSVs before publishing: 82.2% formula-driven, $6.606B operational, 19 function areas. Verified live at www.carolinaredesign.com after the Pages build (~40s).

### 2026-08-04

- **Nav streamlined 8 → 6 items** across all six top-level pages (`index`, `strategy`, `operations`, `agents`, `websites`, `assessment`). New order everywhere: Strategy · Operations · Web & Agents · Assessment · Research · [CTA]
- **Decision: keep `/strategy/`.** User asked whether to delete it as redundant with Operations + Assessment. It isn't — it's Practice 01 on the homepage (with its own card + CTA) and it's the only page carrying the differentiating proof (Palmetto ZBB, ministry diagnostic, clinical cybersecurity, SCAIO). Operations targets ops managers in manufacturing/field-service; Assessment is the $999 productized entry offer. Three rungs of one ladder, not three names for one thing
- **The actual redundancy was Websites + Agents.** The homepage already calls Practice 03 "Web & Agents" (one practice) while the nav gave it two slots, and the two pages cross-sell each other. Merged into a single nav item → `/websites/`, which is the better hub (Foundation/Workforce/Engine already covers agents as "The Workforce", plus the industry demo cards and a primary "Explore Agents" button). `/agents/` stays live, reachable from that button, the homepage footer, and its own breadcrumb (now `Carolina Redesign / Web & Agents / AI Agents`)
- **About moved out of nav into a new homepage footer link row** (Strategy · Operations · Websites · AI Agents · Assessment · Research · About · Contact). It was only ever a `#about` anchor competing for a top-level slot
- **Research added to subpage navs** — previously homepage-only, so navs now match across the site
- **Renamed strategy card `Operational Diagnostics` → `Decision Briefings`** (eyebrow `01 / DIAGNOSTIC` → `01 / BRIEFING`). The old name collided by word with Operations and by concept with Assessment; the card copy was already describing a leadership brief
- **Root cause of the logo collision was CSS, not item count** — fewer items alone didn't fix it. Added to all five hand-rolled navs: `gap: 40px` on `.nav-flex`, `margin-left: auto` on `.nav-links`, `white-space: nowrap` on nav links (stops "Web & Agents" wrapping to two lines), and a mid-desktop `@media (max-width: 1120px)` block that shrinks the logo, gap, and link size before the 768px mobile breakpoint. **Gotcha:** the media query must sit *after* the base `.nav-links a` / `.btn-nav` rules — inserted before them it was silently overridden by equal-specificity later rules
- Verified headless at 1280/1100/1024 on all six pages + mobile hamburger at 390px: no collision, no wrap, mobile menu intact
- Not pushed — repo is public GitHub Pages, awaiting user confirmation

### 2026-07-31

- Replaced `/assessment/index.html` with the user's redesigned sales page (from Downloads): tool-swarm hero animation, leak-list stakes section, 7-item deliverable stack, founder bio card, FAQ, scroll-reveal animations. Direction change from v1: **checkout-first flow** (buy → then 15-min intake) instead of call-the-line-first; page pitches a 45-min walkthrough + 90-day sequence as part of the deliverable
- Applied 8 copy tweaks per user: "which ones" framing in h1/sub (de-emphasized "six"), "AI is revolutionizing businesses every day…" stakes h2, guarantee reworded to **"at least 5 hours of time savings per week or full refund"**, "Business owners" (dropped "with a team"), delivery promise **3 business days → 48 hours** (both spots), bio h2 "We map your workflows and provide a clear AI roadmap," closing line "You're buying judgement and clarity, not software"
- Verified headless (desktop + mobile, reduced-motion pass to render `.reveal` sections): all sections populate, zero JS errors
- **Checkout live**: user created the "AI Assessment - Carolina Redesign" product + $999 payment link in the Stripe dashboard (Secursion Stripe account `acct_1SYgPtJG3emK5MYF` — checkout/statement will show that account's branding). Link `plink_1TzS8TJG3emK5MYF2hwLnIk7` → https://buy.stripe.com/4gMeVed1T6bw4Je5Fq6Zy05. After-payment redirect set via API (restricted key from Railway secursion/vending had payment-link write but NOT product write) → `/assessment/start/`, a new post-checkout page built this session: call Reese (843) 892-4433, 15-min interview, 48-hr delivery, walkthrough scheduling, human-fallback contact. Both CTAs wired to the payment link
- Swarm caption de-sixed per user ("A handful of these… / Probably not the ones…"); "Six moves" + "Six dimensions" kept — they describe the actual report contents

### 2026-07-29

- Built the public marketing page for the AI Opportunity Assessment at `/assessment/index.html` — hero with the Reese intake line CTA (call (843) 892-4433, number pulled live from Vapi since it isn't recorded in the repo), 3-step how-it-works, six report-deliverable cards matching template v2.2 sections (snapshot / map / scorecard / quick wins / the math / safe-use), the three caller segments (smb/exec/npo), and a "ground rules" section (AI disclosure + consent, interviewer-not-advisor, human review). No pricing shown — none is published anywhere; CTA falls back to the contact form for scope/pricing questions
- Wired two entry points: homepage `.assessment-strip` callout after the practices grid, and a "Start with the AI Opportunity Assessment →" link in the strategy page's Diagnostic build card
- Added "Assessment" to the top nav on all six navbar pages (home, strategy, operations, agents, websites, assessment) and **published the price: $999 flat** (user's call, 2026-07-29) — shown in the assessment hero and closing CTA box. Fixed `.btn-nav` wrapping (missing `white-space: nowrap`) on the strategy + assessment navbars now that the nav has an extra item; all navbars re-verified headless at 1280px
- Verified headless (desktop 1280px + mobile 390px full-page screenshots + homepage strip): layout, stacking, and CTAs all render correctly
- Uncommitted at session end: `assessment/index.html` (new), `index.html`, `strategy/index.html`, ATLAS.md — plus the pre-existing assessment-pipeline edits noted below
- Published Palmetto Ledger Issue 2 "The Incremental State" (built in the palmetto-zbb project): added `/palmetto-ledger/the-incremental-state.html`, new `/palmetto-ledger/index.html` series landing page (both issues + Issue 3 teaser), Issue 1 footer cross-link, research-index card now points to the landing page with an "Issue 2" chip. Commit `06aded2`, rebased over the remote Chapin/Brighton commits, pushed, live-verified.
- Note: the push also carried 4 previously-unpushed local commits from the AI-assessment work (`45af020`…`b29c16b`); diff was secret-scanned before pushing (clean). Working tree still has uncommitted assessment-related edits (report_gen.py, templates, this file).

### 2026-07-20

- User reviewed the first real report — verdict "great" — and requested an upfront quick-wins + ROI snapshot. Template bumped **v2.1 → v2.2**: hero now carries a 4-tile snapshot strip (quick-win count · weekly hours returned · monthly tool cost · monthly net ROI) plus a "details are all below" note linking to #wins
- Design decision: the snapshot is rendered by JS that mirrors the Impact section's `.fin` cards and `QUICKWINS.length` — zero new data arrays or editable copy blocks, so the generator/spec content requirements are unchanged and the hero numbers can never disagree with The Math section
- Version string bumped to `template v2.2` in the template footer, spec §7 footer line, report_gen.py SYSTEM_ROLE, and the /build-assessment skill; assets re-synced (`sync_assets.sh`) and Railway redeployed (SUCCESS) — all future auto-drafts include the snapshot
- Retrofitted the snapshot into the user's own populated report, verified headless (tiles: 6 wins · 9 hrs · ~$198 · +$2,250, zero JS errors), uploaded as `assessment-carolina-redesign-v2.2.html` to the Airtable row and pruned the old attachment
- Uncommitted at session end: template, spec, report_gen.py, SKILL.md, assets, caroline_build.py (from 2026-07-19), ATLAS.md

### 2026-07-19

- First REAL end-to-end run (user's own intake call, 2026-07-18): webhook + Telegram + auto-draft all fired; draft attached to the Airtable row. User reported it "not filled out" — diagnosis: the draft is fully populated (all six arrays, scan-signals, safe-use card, zero Tidewater placeholders, renders clean in headless Chromium with 6 quick-win cards + scorecard) — **Airtable's attachment preview doesn't execute JavaScript**, and the template renders nearly everything client-side, so it looks empty there. Correct viewing: download the attachment, open in a browser
- Real bug #1 found + fixed: Vapi structured-data extraction NEVER ran (structuredDataPromptTokens = 0 on both real calls; Airtable rows show Business Name "Unknown", Structured Data `{}`). Cause: `structuredDataPlan.messages` override was a single system message with `{{transcript}}` and no `{{schema}}`. Fixed in `caroline_build.py` to mirror Vapi's default shape (system = guidance + `{{schema}}`, user = `{{transcript}}` + `{{endedReason}}`), PATCHed live (HTTP 200, verified)
- Real bug #2 found + fixed: the intake call ended `exceeded-max-duration` at the 1400s cap — the interview was cut off mid-call. `maxDurationSeconds` raised to 2700 (45 min), PATCHed live
- The auto-draft handled the empty extraction gracefully (generated from transcript alone — quality looked strong: personalized scorecard notes, real scan findings, L6 verbatim intact)
- Housekeeping noted, not done: two stray Airtable rows (a 0-second and a 68-second call) sit at "Ready for Report"; extraction fix unverified until the next call; caroline_build.py change uncommitted

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
