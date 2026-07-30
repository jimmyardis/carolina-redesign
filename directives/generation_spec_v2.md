# Carolina Redesign — AI Assessment Generation Spec v2.1 (Interactive Page)
v2.1 · 2026-07-06 · Consumer: HyperAgent research agent
Supersedes v2.0. Changelog v2.1: readiness scorecard section, implementation path tags,
tool alternatives, safe-use starter, enriched build cards — per taxonomy v1.1. Template
changes required: see §7 (Claude Code work list).
Supersedes v1 (9-slide deck). The deck is retired as the deliverable; it may return later as a
walkthrough-call screen-share generated from the same data arrays.

---

## 1 · Inputs (all three arrive per run; never use a cached copy)

1. **Intake JSON** — schema per `directives/intake_script_v2.md` §8 (transcript attached).
2. **`directives/opportunity_taxonomy.md`** — the ONLY source of what may be recommended,
   how items are gated, scored, and placed (taxonomy §§2–4), and the drop-in language (§6).
3. **Public-data scan** — run fresh per client: website + tech stack (BuiltWith/Wappalyzer),
   Google Business Profile + review themes, social footprint, competitor ad presence (SpyFu).
   Scan findings must appear in the deliverable (§3, section 2) — never scan-and-discard.

## 2 · The prime rule: fixed template, variable data

The deliverable is the approved single-file interactive HTML template
(`templates/assessment_interactive.html` — canonical copy in the repo). The agent does NOT
redesign, restyle, or restructure it. Per client, the agent edits exactly two things:

1. **The six data arrays** at the top of the `<script>` block:
   - `NODES` — 7 objects: `{id, name, cls: leak|win|build|steady, tag, today, quote, cost, move, tools}`
     — populated from intake `nodes[]` using the segment's archetype list (taxonomy §5).
     `today`/`cost`/`quote` come from the client's intake; `quote` is their words, lightly cleaned.
   - `SCORECARD` — 6 objects: `{dimension, score: 1-5, note}` plus `{stage: "S0|S1|S2|S3",
     stage_label}` — scored per taxonomy §4.2; `note` is one plain-English line per dimension.
   - `QUICKWINS` — exactly 6: `{tool, node, use, cost, setup, saves, path: "DIY|Guided DIY",
     alt}` — real, named, verified products (rules §4 below). `alt` is one line: alternative
     tool + the condition under which it wins ("Goodcall — if you'd rather have a human-
     sounding receptionist model trained per location"). Every win has exactly one `alt`.
   - `BUILDS` — exactly 3: `{id: A|B|C, name, nodes[], txt, why, path: "Done-With-You|
     Done-For-You", risk, metric}` — `why` must cite the client's stated pain or the
     gate-unlock logic in plain words; `risk` is one honest watch-out line; `metric` is the
     one number that proves it worked ("days-to-paid drops below 15").
   - `SCATTER` — all placed opportunities: 6 wins (teal), 3 builds (gold), 1–2 ignore items
     (gray). Coordinates: x = effort, y = impact, quadrant-consistent with placements.
   - `BARS` — per-tool weekly hours; MUST sum to the hero hours figure.
2. **The copy blocks** marked editable: hero (name, city, meta row, headline stat), why-section
   stats, scan-signals strip, set-aside block, paths content, footer date.

Everything else — CSS, layout, interactions, section order — is frozen. Template changes are a
human decision, made in the repo, version-bumped. If the agent believes the template itself
needs a change, it flags the suggestion in its run notes; it does not improvise.

## 3 · Section-by-section content spec

1. **Hero** — client first name, business, city, date. Meta row: business type + size /
   Primary Focus (one line, from `top_pain`) / The Headline (hours-per-week + tool cost).
   Remove the SAMPLE pill for real clients.
2. **Why this exists** — drop-in L1 (three lanes intro), the three stat cards (30k-tools framing
   stays; middle card = this client's item count; third = realistic go-live speed), the
   illustrative curve (unchanged), and the promise box. **Scan signals:** 1–2 concrete
   public-scan findings ("From your reviews… / From your site…"), each motivating a quick win.
3. **The map** — 7 nodes from `NODES`, segment archetypes, color classes assigned by placement
   (leak = pain the wins fix now; win = quick-win node; build = bigger-play node; steady =
   running fine). **At least one `steady` node is mandatory** (trust signal). Section intro
   names the segment metaphor (pipeline / week / mission cycle).
3a. **Where you stand (readiness scorecard)** — immediately after the map: six labeled bars
   (1–5) from `SCORECARD`, one plain-English note each, the maturity-stage chip ("Overall:
   Stage 1 · Capture"), and the taxonomy §4.2 disclaimer verbatim. This section is the visible
   bridge between the map (what we saw) and the gates (why some things wait). Never rendered
   as a radar chart; never more than one line of commentary per dimension.
4. **Opportunities** — scatter + numbered list + **the set-aside block**: drop-ins L2a (gated,
   with this client's actual gate stated in their facts — e.g. "calls after 6pm go to
   voicemail") and/or L2b (not applicable), plus L3 (right-order principle). Gated items:
   never quick wins; gray on scatter or one-line in set-aside with the unlock named. The
   set-aside block references the scorecard stage chip where it strengthens the logic.
5. **Quick wins** — 6 cards, every card tagged to a node (`Fixes node N`), **path badge
   (DIY or Guided DIY)**, cost / setup / saves, and the one-line `alt` ("Also fits: …").
   Help strip is replaced by drop-in **L6 verbatim** (the "or a similar implementation
   partner" language — the trust anchor of the whole report).
6. **Bigger plays** — 3 cards tied to nodes; gate-unlockers ranked first and their compounding
   effect stated in `why` ("unlocks X and Y on your map"). Each card renders its **path badge
   (Done-With-You / Done-For-You)**, its `risk` line ("Worth knowing: …") and its `metric`
   line ("It worked if: …").
7. **Impact** — three fin cards + bars + the reconciliation note. Math per taxonomy quantify-by
   hints; conservative; assumptions written out in the note.
7a. **Safe-use starter** — one compact card between Impact and Paths, populated per drop-in
   L7: green light / human review first / keep out of AI tools (their actual sensitive data
   types from intake) / one rule to start (the single most relevant rule for this client).
   One card, four rows, never more.
8. **Two paths** — BOTH CTAs are the walkthrough call (DIY track / done-for-you track); paths
   note = drop-in L5. Never reintroduce a non-call primary CTA.
9. **Footer** — prep date + an HTML comment: `<!-- taxonomy vX.X · intake vX.X · spec v2.0 -->`
   for run traceability.

## 4 · Content rules (carried from v1, still binding)

- Practical and honest, zero hype. Genuinely useful if they never hire us — that's what converts.
- **Real named products only.** Never generic capabilities ("AI Receptionist" is invalid; "Rosie"
  is valid). Taxonomy tool-classes are anchors — verify current best fit via Futurepedia /
  There's An AI For That / web search; confirm the product exists and fits the segment.
- Voice agent never prescribed tools; all recommendations originate here.
- Reference ≥3 intake specifics; every node quote is theirs, not invented.
- SMB lens = operational; EXEC lens = personal leverage (inbox, calendar, triage, decisions);
  NPO lens = mission capacity (funding, programs, reporting).
- ROI: conservative blended rate ($50/hr default), stated assumptions, floor-not-ceiling framing.

## 5 · QA rubric (gate before delivery; ramp review → nudge → auto-deliver)

1. Every tool is a real, named, verified product fitting the segment — zero hallucinated apps,
   zero generic capability labels.
2. Six quick wins, each node-tagged and DIY-viable; true customs live in Bigger Plays only.
3. All 7 nodes populated with today/cost/quote from intake; ≥1 node marked running-fine.
4. ≥3 intake specifics referenced; quotes are the client's own words.
5. ≥1 public-scan finding appears, tied to a quick win.
6. **Gate logic check:** every gate that fires from `gate_probes` is respected (no gated item
   among the wins) AND explained in the set-aside block with the unlock named, in client-
   checkable plain language.
7. Math reconciles: BARS sum = hero hours; tool-cost total = sum of six cards; hero figures
   match everywhere they appear; assumptions stated.
8. Both path CTAs point to the walkthrough call; L5 language present.
9. Template untouched outside data arrays + editable copy blocks (diff against canonical
   template to verify).
10. Tone honest and DIY-viable; business facts accurate; no PII beyond first name + business;
    version comment present in footer.
11. Scorecard present with all six dimensions, stage chip consistent with fired gates, and the
    directional disclaimer verbatim — a Stage 1 chip with amplify-lane quick wins is a FAIL.
12. Every quick win carries a valid path (DIY/Guided DIY) and exactly one `alt` line naming a
    real, verified alternative + its condition; every build carries path + risk + metric.
13. L6 present verbatim (including "or a similar implementation partner"); safe-use card
    present with restricted-data row reflecting THIS client's stated sensitive data — a
    generic restricted list is a FAIL.

Any failure → report does not send; agent logs which gate failed and why.

## 7 · Template change list (Claude Code — one-time work on templates/assessment_interactive.html)

The following template modifications implement this spec version. After these land, re-freeze
the template as canonical and diff against it per QA #9.

1. **New section 3a "Where you stand"** after the map section (dark→light boundary): renders
   `SCORECARD` as six horizontal bars (reuse `.bar-row` pattern, 1–5 scale), one `note` line
   per dimension, a stage chip styled like the existing badges, and the disclaimer in
   `.fin-note` styling. Add nav link "Where you stand".
2. **Quick-win cards**: replace the DIY badge with a path badge (`b-win` styling for DIY,
   a new `b-guided` variant — same teal family, outlined); add an `alt` line under the meta
   row: `.qw .alt` — 12.5px, `--tx-faint`, prefixed "Also fits: ".
3. **Help strip**: swap current copy for drop-in L6 verbatim (keep the strip's visual shell).
4. **Build cards**: add path badge next to the letter chip; add two lines above the `why`
   border: "Worth knowing: {risk}" and "It worked if: {metric}" — 13px, `--cream-dim`.
5. **New safe-use card** between Impact and Paths: single `.why-close`-style card, four rows
   (Green light / Human review first / Keep out of AI tools / One rule to start), row labels
   in `IBM Plex Mono` caps, teal for green-light, rust for keep-out.
6. **Data arrays**: extend per §2 (SCORECARD added; QUICKWINS + `path`,`alt`; BUILDS +
   `path`,`risk`,`metric`) with render code reading the new fields; placeholder data in the
   canonical template.
7. Bump footer version comment format to include template version:
   `<!-- template v2.2 · taxonomy v1.1 · intake v2.1 · spec v2.1 -->`.

## 6 · Delivery & self-annealing

- SLA: report in the client's inbox within 48 hours of intake completion.
- Run notes per report: tools considered/rejected, gates fired, QA results, any template-change
  suggestions. Review notes every 10 reports; feed learnings to taxonomy §7 and this spec;
  bump versions on change.
