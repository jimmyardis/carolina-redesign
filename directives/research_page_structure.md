# Directive: Research Page Structure (Palmetto Ledger + Palmetto Field Notes)

## Goal
Publish the Carolina Redesign research section as two named collections, each holding several formats, with stable URLs that survive renumbering and a later move to another domain (possibly Trellis).

- **Palmetto Ledger:** public finance and budget research (existing).
- **Palmetto Field Notes:** environment and natural resources research (new). Its first content is the three Living Models.

## Before You Start
1. Inspect the existing site repo: framework or static setup, where `/research/` currently lives, and how Palmetto Ledger pages are linked. Match existing conventions (nav, header/footer, styles) on the landing pages only. The individual model pages are self-contained and stay as they are, apart from the header edits below.
2. Do not delete or move existing Palmetto Ledger URLs. Only add to them, plus the cross-listing badge where noted.

## URL Structure
Numbers never appear in URLs. They appear only in page headings and card labels.

```
/research/                                  → research landing (two collection cards)
/research/palmetto-ledger/                  → existing Ledger content (unchanged paths)
/research/field-notes/                      → Field Notes landing
/research/field-notes/models/cod-commons/
/research/field-notes/models/breathing-marsh/
/research/field-notes/models/redfish-slot/
/research/field-notes/atlases/coastal-time-machine/       (when built)
/research/field-notes/observatories/soundscape/           (when built)
/research/field-notes/ledgers/conservation-ledger/        (when built; cross-listed)
```

Source folders to rename on import:

**Important: the Cod Commons source is the v1 build, not the zip.** Use the built page from the `commons-models` repo (`dist/`). The zip's `living-models-01-cod-commons` file is the superseded prototype and contains two known factual errors (the 1968 catch figure and the 1970 quota date). Do not publish it anywhere. If the v1 page lacks the series line and footer, add them per "Header Edits" below.

| From | To |
|---|---|
| `commons-models/dist/` built page (v1) | `research/field-notes/models/cod-commons/index.html` |
| `living-models-02-breathing-marsh/index.html` | `research/field-notes/models/breathing-marsh/index.html` |
| `living-models-03-redfish-slot/index.html` | `research/field-notes/models/redfish-slot/index.html` |

If any `living-models-0X-*` URLs were already live, add redirects (301) to the new paths using the host's mechanism (`_redirects`, `netlify.toml`, `vercel.json`, or meta-refresh fallback for plain static hosting).

## Header Edits on Each Model Page
Each page currently shows a series line reading "Carolina Redesign Research" with a "Living Models, No. X" badge. Change it to:
- Line text: `Palmetto Field Notes`, linked to `/research/field-notes/`
- Badge: unchanged (`Living Models, No. X`)
- Footer: "… is No. X in Living Models, part of Palmetto Field Notes from Carolina Redesign Research." Keep the byline and date line.
- `<title>`: `{Title} | Living Models No. X | Palmetto Field Notes`

Change nothing else in these files. They are self-contained, fully tested pages.

## Catalog Data (single source of truth)
Create `research/catalog.json`. Both landing pages render their cards from this file, so adding a project means adding one entry.

```json
[
  {
    "slug": "cod-commons",
    "title": "The Cod Commons",
    "collection": ["field-notes"],
    "format": "model",
    "number": 1,
    "path": "/research/field-notes/models/cod-commons/",
    "summary": "A playable model of the Northern cod collapse, checked against the published record.",
    "place": "elsewhere",
    "themes": ["fisheries"],
    "status": "live",
    "published": "2026-09"
  },
  {
    "slug": "breathing-marsh",
    "title": "The Breathing Marsh",
    "collection": ["field-notes"],
    "format": "model",
    "number": 2,
    "path": "/research/field-notes/models/breathing-marsh/",
    "summary": "A salt marsh at Edisto Beach, drawn at the real height of the tide.",
    "place": "coast",
    "themes": ["tides-coast"],
    "status": "live",
    "published": "2026-09"
  },
  {
    "slug": "redfish-slot",
    "title": "The Redfish Slot",
    "collection": ["field-notes"],
    "format": "model",
    "number": 3,
    "path": "/research/field-notes/models/redfish-slot/",
    "summary": "Set South Carolina's red drum rules yourself and watch what happens to the spawners.",
    "place": "coast",
    "themes": ["fisheries"],
    "status": "live",
    "published": "2026-09"
  },
  {
    "slug": "coastal-time-machine",
    "title": "Coastal Time Machine",
    "collection": ["field-notes"],
    "format": "atlas",
    "number": 1,
    "path": null,
    "summary": "How South Carolina's shoreline and marshes have moved since the 1850s.",
    "place": "coast",
    "themes": ["tides-coast"],
    "status": "in-progress",
    "published": null
  },
  {
    "slug": "conservation-ledger",
    "title": "Conservation Ledger",
    "collection": ["field-notes", "palmetto-ledger"],
    "format": "ledger",
    "number": 1,
    "path": null,
    "summary": "What South Carolina has paid to conserve, and what it protects.",
    "place": "statewide",
    "themes": ["forests", "water", "tides-coast"],
    "status": "in-progress",
    "published": null
  },
  {
    "slug": "soundscape",
    "title": "Soundscape Observatory",
    "collection": ["field-notes"],
    "format": "observatory",
    "number": 1,
    "path": null,
    "summary": "Listening to South Carolina's habitats, starting at Botany Bay.",
    "place": "coast",
    "themes": ["wildlife"],
    "status": "planned",
    "published": null
  }
]
```

### Allowed values
- `format`: `model` (Living Models), `atlas` (Atlases), `observatory` (Observatories), `ledger` (Ledgers)
- `place`: `coast`, `midlands`, `upstate`, `statewide`, `elsewhere` (displayed as "Case study from elsewhere")
- `themes`: `fisheries`, `tides-coast`, `forests`, `water`, `wildlife`
- `status`: `live`, `prototype`, `in-progress`, `planned`

## Card and Badge Rules
- Card shows: format + number ("Living Models, No. 3"), title, summary, place tag, status badge.
- Only `live` and `prototype` cards link. `in-progress` and `planned` cards render muted, with no link, under a "Coming" subheading at the end of their format group.
- An entry in both collections shows on both landing pages, with a small "Also in Palmetto Ledger" or "Also in Field Notes" badge on the card.
- `place: elsewhere` must show its label on the card, so nobody assumes the Cod Commons is about South Carolina.

## Landing Pages
**`/research/`**
- One-line intro: independent research on South Carolina's public money and natural resources.
- Two large collection cards: Palmetto Ledger ("Following the state's money") and Palmetto Field Notes ("Notes from the land and water").

**`/research/field-notes/`**
- A short intro paragraph in plain, first-person-plural naturalist voice. No mission-statement jargon.
- The newest `live` item featured at the top.
- Then items grouped by format, in this order: Living Models, Atlases, Observatories, Ledgers. Within each group, sort by number.
- Optional filter chips by place and theme (client-side, reading `catalog.json`). Skip them until there are more than about six live items.

## Portability (possible move to Trellis)
- All research content lives under `/research/`, with no dependencies outside it except shared site chrome on the two landing pages.
- Model pages must not link to non-research Carolina Redesign pages, except the byline. This keeps the folder copyable as-is.
- If the move happens, it should be a folder copy, a redirect rule (`/research/*` → new domain), and a byline edit.

## Verification
1. Every path in `catalog.json` with status `live` resolves and returns 200.
2. Each model page loads with no console errors on a 390px mobile viewport, in both light and dark mode.
3. The Breathing Marsh's tide data runs through March 2027. Add a reminder (calendar entry or a TODO in the repo README) to refresh it by February 2027.
4. Old `living-models-0X-*` paths redirect, if they were ever live.

## Learnings Log
- 2026-10-02: Host is GitHub Pages (plain static, CNAME www.carolinaredesign.com). No `_redirects`; use meta-refresh pages.
- The Ledger was never under `/research/`: it lives at `/palmetto-ledger/`. Left in place (URLs unchanged); `/research/palmetto-ledger/` is a meta-refresh to it. So the Ledger is NOT inside the portable `/research/` folder.
- No `living-models-0X-*` path was ever committed here, so no redirects were needed.
- Model pages are generated by `commons-models` (`build_model.py` then `export_site.py`); never hand-edit them in this repo. The Marsh and Redfish pages were rebuilt with the Cod treatment (sourced data, fits, citation gate), so they differ from the zip versions beyond the header edits.
- Landing pages render client-side from `catalog.json` via `research/catalog.js`; a `<noscript>` fallback lists the live models.
- The research landing keeps Urban Productivity as a small "Also from our research" link so it isn't orphaned.
