// Research catalog: renders cards from /research/catalog.json, the single source of truth for
// Palmetto Field Notes, Palmetto Plat, and the Palmetto Ledger cross-list.
// Adding a project = adding one entry. Format numbers run globally, not per collection,
// so "Ledgers, No. 2" means the same thing on every landing page.
(function () {
  const FORMATS = {
    model: { group: "Living Models", one: "Living Models" },
    atlas: { group: "Atlases", one: "Atlases" },
    observatory: { group: "Observatories", one: "Observatories" },
    ledger: { group: "Ledgers", one: "Ledgers" },
  };
  const FORMAT_ORDER = ["model", "atlas", "observatory", "ledger"];
  const PLACES = { coast: "Coast", midlands: "Midlands", upstate: "Upstate", statewide: "Statewide", elsewhere: "Case study from elsewhere" };
  const STATUS = { live: "Live", prototype: "Prototype", "in-progress": "In progress", planned: "Planned" };
  const COLLECTIONS = { "field-notes": "Field Notes", "palmetto-ledger": "Palmetto Ledger", "palmetto-plat": "Palmetto Plat" };
  // Themes are per-collection vocabularies; listed here so a card can label one.
  const THEMES = {
    fisheries: "Fisheries", "tides-coast": "Tides & coast", forests: "Forests",
    water: "Water", wildlife: "Wildlife",
    connectivity: "Connectivity", transportation: "Transportation",
    "land-use": "Land use", "fiscal-productivity": "Fiscal productivity",
  };
  const LINKABLE = (e) => (e.status === "live" || e.status === "prototype") && e.path;

  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function card(e, here, featured) {
    const label = `${FORMATS[e.format].one}, No. ${e.number}`;
    const also = e.collection.filter((c) => c !== here).map((c) => `<span class="rc-badge rc-also">Also in ${COLLECTIONS[c]}</span>`).join("");
    const body = `
      <p class="rc-label">${label}</p>
      <h3 class="rc-title">${esc(e.title)}</h3>
      <p class="rc-summary">${esc(e.summary)}</p>
      <p class="rc-tags"><span class="rc-badge rc-place rc-place-${e.place}">${PLACES[e.place]}</span><span class="rc-badge rc-status rc-${e.status}">${STATUS[e.status]}</span>${also}</p>`;
    const cls = `rc-card${featured ? " rc-featured" : ""}${LINKABLE(e) ? "" : " rc-muted"}`;
    return LINKABLE(e) ? `<a class="${cls}" href="${e.path}">${body}</a>` : `<div class="${cls}" aria-disabled="true">${body}</div>`;
  }

  // Items grouped by format (fixed order), sorted by number; unlinked items under "Coming" at the end of their group.
  function groups(items, here) {
    return FORMAT_ORDER.map((f) => {
      const all = items.filter((e) => e.format === f).sort((a, b) => a.number - b.number);
      if (!all.length) return "";
      const ready = all.filter(LINKABLE), coming = all.filter((e) => !LINKABLE(e));
      return `<section class="rc-group"><h2 class="rc-group-title">${FORMATS[f].group}</h2>
        ${ready.length ? `<div class="rc-grid">${ready.map((e) => card(e, here)).join("")}</div>` : ""}
        ${coming.length ? `<h3 class="rc-coming">Coming</h3><div class="rc-grid">${coming.map((e) => card(e, here)).join("")}</div>` : ""}
      </section>`;
    }).join("");
  }

  function newestLive(items) {
    const live = items.filter((e) => e.status === "live" && e.published);
    return live.reduce((best, e, i) => (!best || e.published >= best.published ? e : best), null);
  }

  async function load() {
    const r = await fetch("/research/catalog.json", { cache: "no-cache" });
    if (!r.ok) throw new Error(`catalog.json returned ${r.status}`);
    return r.json();
  }

  window.ResearchCatalog = { load, card, groups, newestLive, LINKABLE, COLLECTIONS, THEMES };
})();
