# Directive — Opportunity Taxonomy & Readiness Gates
v1.1 · 2026-07-06 · Consumer: HyperAgent research agent
Changelog v1.1: added implementation paths (§4.1), readiness scorecard (§4.2), safe-use pack
rules + drop-ins L6/L7 (§6), per market teardown of competing assessment products.

Layer 1 instruction set for the AI Opportunity Assessment research agent. This is the master
checklist the agent scans on EVERY assessment, the gate rules that decide what the report
spends time on, and the drop-in language that explains those decisions to the client.

**Prime rule: comprehensive scan, selective report.** The agent checks every item below for
every client. The report shows only what scored — plus a visible, honest account of what we
deliberately set aside and why. The filter IS the product.

---

## 1 · The model: three lanes and a rail

Every business, HVAC shop to law firm, runs three lanes of work plus a nervous system underneath:

| Code | Lane | Plain description |
|---|---|---|
| D | **Get customers** | Demand: being found, making noise, filling the pipeline |
| O | **Serve customers** | Operations: answering, scheduling, doing the work, getting paid & reviewed |
| B | **Run the business** | Back office: books, people, compliance, knowledge, visibility |
| R | **The rail** | Information routing under all three: everything lands where it belongs, automatically |

Executives and nonprofits use the same model with different node vocabularies (§5).

---

## 2 · Master taxonomy

Applicability: ● primary fit · ○ sometimes · — rarely/never. Segment columns: SMB / EXEC / NPO.
"Typical form" = DIY (off-the-shelf app), LIGHT (Make.com-grade automation), BUILD (Tier 2 custom).

### Lane D — Get customers

| ID | Opportunity | SMB | EXEC | NPO | Typical form | Quantify by |
|---|---|---|---|---|---|---|
| D1 | Website presence & AI content refresh | ● | — | ● | DIY/BUILD | leads/mo |
| D2 | Local SEO & Google Business Profile upkeep | ● | — | ○ | DIY | ranking, calls/mo |
| D3 | Content & social — generate, schedule, repurpose job media | ● | ○ | ● | DIY (Metricool-class) | hrs/wk + reach |
| D4 | Paid ads management — variants, fatigue detection, auto-pause | ● | — | ○ | DIY (Revealbot-class) | CAC, $/mo |
| D5 | Lead scraping & list building | ● | ○ | ○ | LIGHT | leads/mo |
| D6 | Cold outreach sequences (email/SMS) | ● | ○ | ○ | DIY (Instantly-class) | booked calls/mo |
| D7 | Referral & partnership nurture loops | ● | ○ | ● | LIGHT | referrals/mo |
| D8 | Estimating & proposals — photo-to-quote, AI-drafted bids | ● | ○ | ○ | DIY/BUILD | quote turnaround, win rate |
| D9 | Reputation — AI-drafted review responses, competitor review watch | ● | — | ○ | DIY | hrs/wk + rating |
| D10 | Competitive & pricing intelligence monitoring | ○ | ○ | ○ | LIGHT | pricing confidence |
| D11 | Grant discovery & drafting *(NPO-primary)* | — | — | ● | DIY/BUILD | $ pipeline |

### Lane O — Serve customers

| ID | Opportunity | SMB | EXEC | NPO | Typical form | Quantify by |
|---|---|---|---|---|---|---|
| O1 | Inbound answering & qualification, 24/7 | ● | — | ○ | DIY (Rosie-class) | leads saved/mo |
| O2 | Speed-to-lead response on web forms | ● | — | ○ | LIGHT | jobs/mo |
| O3 | FAQ deflection — site/SMS assistant | ● | — | ● | DIY (Chatbase-class) | hrs/wk |
| O4 | Scheduling, dispatch & reminders platform | ● | — | ○ | DIY (Housecall-class) | hrs/wk, no-shows |
| O5 | Job documentation — photos/notes auto-filed to job record | ● | — | ○ | LIGHT | disputes, marketing feed |
| O6 | Customer status comms — on-my-way, progress, completion | ● | — | ○ | DIY | calls deflected |
| O7 | Review collection after every job | ● | — | ○ | DIY (NiceJob-class) | reviews/mo |
| O8 | Warranty / maintenance-plan tracking & renewal outreach | ● | — | — | LIGHT/BUILD | recurring $/mo |
| O9 | Field knowledge assist — techs query pricing & SOPs | ● | — | ○ | BUILD | callbacks, ramp time |
| O10 | Volunteer / program coordination *(NPO-primary)* | — | — | ● | DIY/LIGHT | hrs/wk |

### Lane B — Run the business

| ID | Opportunity | SMB | EXEC | NPO | Typical form | Quantify by |
|---|---|---|---|---|---|---|
| B1 | Bookkeeping & expense capture — receipt photo → categorized | ● | ● | ● | DIY (Dext/Ramp-class) | hrs/mo |
| B2 | AR & collections — polite automated invoice chasing | ● | — | ○ | LIGHT | days-to-paid, $ float |
| B3 | Payroll & job costing | ● | — | ○ | DIY | hrs/mo, margin visibility |
| B4 | Tax document funnel — docs routed to the accountant folder | ● | ● | ● | LIGHT | tax-season hrs |
| B5 | Hiring — posts, resume screen, interview scheduling | ● | ○ | ● | DIY | days-to-hire |
| B6 | Training & SOP knowledge base — queryable, not a binder | ● | ○ | ● | BUILD | ramp time, key-person risk |
| B7 | Inventory, parts ordering, supplier price watch | ● | — | — | LIGHT | stockouts, $/mo |
| B8 | Compliance calendar — licenses, permits, insurance renewals | ● | ○ | ● | LIGHT | risk avoided |
| B9 | Cash-flow & KPI dashboard — the Monday-morning number | ● | ○ | ● | LIGHT/BUILD | decision speed |
| B10 | Contract & document review assist | ○ | ● | ○ | DIY | hrs + risk |
| B11 | Meeting capture & action tracking | ● | ● | ● | DIY (Fathom-class) | hrs/wk |
| B12 | Forecasting — jobs, revenue, seasonality | ○ | ○ | ○ | BUILD | planning confidence |
| B13 | Board & funder reporting *(NPO-primary)* | — | — | ● | LIGHT/BUILD | hrs/quarter |

### The rail — R

| ID | Opportunity | SMB | EXEC | NPO | Typical form | Quantify by |
|---|---|---|---|---|---|---|
| R1 | Intake router — receipts→books, photos→job+social, voicemail→tasks, docs→tax | ● | ● | ● | BUILD | hrs/wk everywhere |
| R2 | Unified CRM / system of record, lead-to-review | ● | — | ● | BUILD | leak rate, visibility |
| R3 | Inbox triage & calendar defense *(EXEC-primary)* | ○ | ● | ○ | DIY/BUILD | hrs/wk |
| R4 | Personal knowledge system — notes, decisions, references *(EXEC-primary)* | — | ● | ○ | DIY/BUILD | recall speed |

**Rail note:** R-items are almost always Tier 2 territory and almost always the highest-compounding
recommendation on the board. They also unlock more gates than anything else (§3) — score them accordingly.

---

## 3 · Readiness gates — the right order beats more tools

Every opportunity gets a readiness check BEFORE it gets ranked. Gating is a hard filter:
a gated item cannot appear as a quick win no matter how well it scores. It appears instead
in "Later — and why," explicitly tied to what unlocks it.

### The maturity ladder

| Stage | Name | The client can honestly say… |
|---|---|---|
| S0 | **Findable** | "People can find us and reach us" — working website, GBP claimed, phone answered in business hours |
| S1 | **Capture** | "Every lead gets answered, qualified, and scheduled — fast, even after hours" |
| S2 | **Amplify** | "We can turn up demand and handle what comes" — marketing, outreach, ads, scraping |
| S3 | **Compound** | "Our systems talk to each other" — rail, CRM, dashboards, forecasting |

### Gate rules

| Gate | If intake/scan shows… | Then gate… | Say it as… |
|---|---|---|---|
| G1 | No functional website / unclaimed GBP | D2–D6, D9 | "Marketing amplifies what exists. Right now there's nothing to point the traffic at — foundation first." |
| G2 | Inbound capture broken (missed calls, no booking path, slow web response) | ALL of D3–D7 amplify spend | "No point making the phone ring louder if nobody's answering it. Fix capture, then amplify." |
| G3 | Books not digitized / no accounting platform | B9, B12 | "A dashboard on top of a shoebox is still a shoebox. Digitize first, then measure." |
| G4 | No system of record (jobs live in texts and memory) | R1 (full), O5, O8 | "The router needs somewhere to route TO. Platform first, rail second." |
| G5 | EXEC: calendar/inbox in chaos, no assistant layer | Deep-work automation, R4 | "Triage before automation — otherwise you're automating chaos." |
| G6 | Team hostile/burned by prior AI rollout (from intake) | Anything team-facing (O9, B6) until a small visible win lands | "One quiet win first. Then the team tools." |

### Two consequences the agent must apply

1. **Gated ≠ hidden.** Gated items appear on the map as gray "Later" nodes and in one short
   "what we set aside and why" block — with the unlock named. This is where comprehensiveness
   shows without noise, and it seeds the NEXT engagement honestly.
2. **Gate-unlockers get a scoring boost.** If a build (say R2, or a website rebuild) would flip
   two or more gated items to available, that compounding effect is stated in its "why it made
   the list" line and boosts its rank. The best infrastructure recommendation is visible logic,
   not a pitch.

---

## 4 · Scoring & report placement

For every ungated item: **score = (monthly impact in hrs or $) × confidence ÷ effort.**
Confidence comes from how directly the client named the pain (their words > our inference > generic).

| Placement | Rule |
|---|---|
| Quick wins (max 6) | Top-scored DIY/LIGHT items, ungated, installable in ≤2 weeks |
| Bigger plays (max 3) | Top-scored BUILD items — gate-unlockers ranked first |
| Running fine | Nodes with no material pain — ALWAYS show at least one (trust signal) |
| Later — and why | Gated items + good-but-not-now, each with its unlock named, one line each |
| Ignore | 1–2 things the client asked about or the market hypes that genuinely don't fit — say so plainly |

Report shows 6 + 3. Everything else is one line or a gray node. Never inflate the count —
the moment the report feels long, the filter promise is broken.

## 4.1 · Implementation paths

Every placed recommendation carries exactly one path label. This replaces the binary DIY /
We-build tag with a graduated scale — and it's where the "hire us or don't" honesty lives.

| Path | Meaning | Typical placement |
|---|---|---|
| DIY | Client installs it themselves with basic comfort and the report's pointers | Quick wins (default) |
| Guided DIY | Client runs it; setup, templates, or an hour of training helps it stick | Quick wins |
| Done-With-You | Partner configures workflows/integrations alongside the client's team | Bigger plays (lighter) |
| Done-For-You | Partner builds and hands over | Bigger plays (heavier) |
| Defer | Gated or premature — named unlock required first | Later — and why |

**Assignment rules:** intake `implementation_preference` biases but does not override the
label — the label reflects what the work honestly requires, not what we'd like to sell.
Quick wins may never carry Done-For-You as their ONLY path; a DIY route must always be
stated. Anything team-facing under gate G6 takes Guided DIY minimum.

## 4.2 · Readiness scorecard

Six dimensions, scored 1–5, rendered in the report between the map and the opportunities.
Scores are directional, derived from intake + public scan — never presented as scientific.

| Dimension | Scored from |
|---|---|
| Strategy & alignment | `success_definition` clarity, `top_pain` specificity |
| Workflow maturity | `gate_probes.sops`, node walk coherence |
| Data & knowledge readiness | `gate_probes.data_org`, `books`, `system_of_record` |
| Technology & integration | public scan tech stack, `online_booking`, platform presence |
| Team capability | `tech_comfort_team`, `team_receptivity`, `prior_ai` |
| Governance & risk posture | `gate_probes.ai_rules`, `sensitive_data`, review habits |

The scorecard also names the client's **maturity ladder stage** (§3) as a single chip —
"Overall: Stage 1 · Capture" — which is the visible link between their scores and why
certain items were gated. Mandatory disclaimer, verbatim:
> Scores are directional — built from your interview, your own words, and your public
> footprint. They exist to prioritize action, not to certify anything.

---

## 5 · Segment overlays

One intake spine, one qualifying question, three node vocabularies. The taxonomy above is
scanned for all segments using the applicability columns.

**Qualifying question (intake, first branch):** "Which best describes you — running a business
with a team, an executive or professional managing your own workload, or leading a nonprofit?"

| Segment | Map metaphor | Node archetypes (the pipeline the report draws) |
|---|---|---|
| SMB | The business pipeline | Lead comes in → Answer & qualify → Schedule & dispatch → The work → Invoice & follow-up → Review & rebook → Run the business |
| EXEC | The working week | Inbox & comms → Meetings → Decisions & info triage → Deep work & deliverables → Delegation & follow-up → Admin & expenses → Learning & network |
| NPO | The mission cycle | Funding in (donors/grants) → Donor & community comms → Program delivery → Volunteers & staff → Compliance & reporting → Board & governance → Run the org |

**Universal catch-all closer (all segments, never skip):** *"What eats your time that I didn't
ask about?"* — answers feed §7.

---

## 6 · Drop-in report language

Verbatim blocks the generator selects from. Personalize the bracketed slots; do not soften the honesty.

**L1 — Three lanes intro (always, in "Why this exists" or atop the map):**
> Everything AI could touch in [business] falls into three lanes: getting customers, serving
> them, and running the business behind it — plus the plumbing that connects all three. We
> scanned every lane. What follows is only what's worth your energy right now.

**L2a — Set aside: gated:**
> A few high-potential areas didn't make this report on purpose. [Example: marketing
> amplification — lead scraping, ads, outreach.] Not because they don't work — because
> sequence matters. [Their gate, in plain words: "Right now, calls after 6pm go to voicemail.
> Turning up marketing would just make the phone ring off the hook unanswered."] Fix
> [unlock], and these move to the top of the next list.

**L2b — Set aside: genuinely not applicable:**
> And some things simply don't fit [business] — [example] — no matter how loudly the AI
> hype cycle says otherwise. We'd rather tell you that than pad the list.

**L3 — The right-order principle (near the map or Later section):**
> The order matters more than the tools. Capture before you amplify. Digitize before you
> measure. Platform before plumbing. Every "later" on your map has a named unlock — when
> that lands, the next opportunities are already queued.

**L4 — Later-list framing:**
> Here's what's waiting behind those unlocks — each one line, so you know the map is bigger
> than this quarter: [gated + deferred items, one line each, unlock named].

**L5 — Paths closer (both paths end in the call):**
> Whichever lane you pick, your assessment includes a 30-minute walkthrough call. If you're
> doing it yourself, we'll walk the map node by node and make sure you know exactly what each
> tool is and where it goes — then you're off. If you want it done for you, we'll scope it on
> the same call, and you'll get a fixed price in writing. Either way: same call, no obligation,
> already paid for. The only bad outcome is this report sitting in a tab.

**L6 — Implementation options (appears once, near the paths; the trust anchor):**
> Most of the quick wins in this report can be implemented internally — that's by design.
> Where a recommendation involves integrations, workflow redesign, or custom builds, outside
> help can save time and reduce risk. That help does not need to come from Carolina Redesign;
> what matters is a partner who understands both your workflow and the practical limits of AI
> systems. **Carolina Redesign, or a similar implementation partner,** can assist where
> helpful — and this report is yours to use independently or hand to any qualified vendor
> or internal team.

**L7 — Safe-use starter (one compact block, personalized; the governance section, entire):**
Render as a four-row card, populated from the client's actual context:
> **Green light:** drafting, summarizing, brainstorming, internal productivity, first-pass
> analysis. **Human review first:** anything sent to a customer, anything involving money,
> personnel, or commitments. **Keep out of AI tools:** [their actual sensitive data types
> from intake — e.g. customer payment details, employee records]. **One rule to start:**
> [the single most relevant rule for THIS client — e.g. "recording consent line before
> Fathom joins a client call"].
SMB/EXEC get exactly this block, nothing more. NPO or regulated clients get one added line
recommending a written AI-use policy before org-wide rollout (a Carolina Redesign build,
tagged honestly per L6). Never let governance exceed one card — the moment it reads like
compliance theater, the filter promise breaks.

---

## 7 · Self-annealing

- **Catch-all mining:** when the closer question surfaces the same missing pain 3+ times,
  add it to §2 with segment flags and a quantify-by. Log the addition date.
- **Tool refresh:** tool-class examples ("Rosie-class") are anchors, not commitments — the
  generator verifies current best-in-class per the generation spec's real-tools rule. Re-verify
  the anchor names quarterly.
- **Gate learnings:** when a client outcome shows a gate fired wrongly (or a missing gate let
  a bad recommendation through), update §3 and note the client case.
- This directive is the single source of truth for WHAT can be recommended. The generation
  spec owns HOW the report renders. The intake script owns HOW the data comes in. Don't let
  taxonomy content drift into the other two.
