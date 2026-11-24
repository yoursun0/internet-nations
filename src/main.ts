import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import "./styles.css";
import { chromeHiddenActive, readHideChrome, writeHideChrome, type ChromeStorage } from "./chrome";
import { parseView, resolveLang, serialize } from "./deeplink";
import { fillFor } from "./fill";
import { graticule } from "./geo";
import { t } from "./i18n";
import { joinCountries, type GeoCollection } from "./join";
import {
  CONTINENTS,
  LAYER_SOURCE_IDS,
  platformName,
  PLATFORMS,
  profileByIso,
  profilesFromDataset,
  REGIONS,
  SOURCES,
  sourceList,
} from "./model";
import { ensurePattern } from "./patterns";
import {
  CATS,
  CONTINENT_ORDER,
  LANG_KEY,
  LAYERS,
  NODATA,
  STACK_COLOR,
  WORLD_BBOX,
  type Lang,
  type LayerId,
  type Profile,
} from "./types";

const $ = <T extends HTMLElement>(id: string) => document.getElementById(id) as T;

const brandTitle = $("brand-title");
const brandEn = $("brand-en");
const kicker = $("kicker");
const yearBadge = $("year-badge");
const langBox = $("lang");
const indexBtn = $("index-btn");
const layersEl = $("layers");
const searchLabel = $("search-label");
const searchInput = $<HTMLInputElement>("q");
const results = $("results");
const searchWrap = $("search");
const regionBtn = $("region-btn");
const regionPop = $("region-pop");
const regionWrap = $("region-wrap");
const crumbs = $("crumbs");
const legend = $("legend");
const panel = $("panel");
const geoFail = $("geo-fail");
const aboutBtn = $("about-btn");
const hideChromeBtn = $("hide-chrome");
const showChromeBtn = $("show-chrome");
const aboutRestoreBtn = $("about-restore");
const tip = $("tip");
const about = $("about");
const indexBox = $("index");
const live = $("live");
const skip = $("skip");
const mapNode = $("map");

const profiles = new Map(profilesFromDataset());
let geoms = new Map<string, { bbox: [number, number, number, number]; label: [number, number] }>();
let map: maplibregl.Map | null = null;
let labelLayer: HTMLDivElement | null = null;
let selectedId: string | null = null;
let hoverId: string | null = null;
let searchActive = 0;
let builtLayers = false;
let builtLang = false;
let hideChromePref = false;
let aboutOpener: HTMLElement | null = null;

function chromeStorage(): ChromeStorage | null {
  try {
    return localStorage;
  } catch {
    return null;
  }
}

function viewportWidth(): number {
  return document.documentElement.clientWidth || window.innerWidth;
}

function chromeIsHidden(): boolean {
  return chromeHiddenActive(hideChromePref, viewportWidth());
}

function syncChromeClass() {
  document.documentElement.classList.toggle("chrome-hidden", hideChromePref);
}

function resizeMapSoon() {
  map?.resize();
  requestAnimationFrame(() => map?.resize());
}

function focusIfShown(el: HTMLElement | null): boolean {
  if (!el || el.getClientRects().length === 0) return false;
  el.focus();
  return true;
}

function setHideChrome(hidden: boolean, focus?: "toggle" | "search") {
  hideChromePref = hidden;
  writeHideChrome(chromeStorage(), hidden);
  syncChromeClass();
  resizeMapSoon();
  if (!focus) return;
  requestAnimationFrame(() => {
    if (focus === "search") {
      searchInput.focus();
      searchInput.select();
      return;
    }
    if (chromeIsHidden()) focusIfShown(showChromeBtn);
    else focusIfShown(hideChromeBtn);
  });
}

const state: {
  lang: Lang;
  layer: LayerId;
  region: string | null;
  continent: string | null;
  fid: string | null;
  filter: string | null;
  about: boolean;
  indexOpen: boolean;
  legendOpen: boolean;
  sheetExpanded: boolean;
} = {
  lang: "zh-Hant",
  layer: "overview",
  region: null,
  continent: null,
  fid: null,
  filter: null,
  about: false,
  indexOpen: false,
  legendOpen: false,
  sheetExpanded: false,
};

function nameOf(id: string, layer: LayerId, lang: Lang): string {
  if (layer === "overview" || STACK_COLOR[id]) return t(lang, `stack.${id}`);
  return platformName(id, lang);
}

function swatchLabel(key: string): string {
  if (key === "nodata") {
    return state.layer === "overview" ? t(state.lang, "stack.unknown") : t(state.lang, "legend.nodata");
  }
  if (key === "inferred") return t(state.lang, "legend.inferred");
  if (key.includes("+")) return key.split("+").map((id) => platformName(id, state.lang)).join(" · ");
  if (STACK_COLOR[key]) return t(state.lang, `stack.${key}`);
  return platformName(key, state.lang);
}

function swatchBackground(key: string): string {
  if (key === "nodata" || key === "inferred") return NODATA;
  if (key.includes("+")) {
    const colors = key.split("+").map((id) => PLATFORMS[id]?.color ?? "#888");
    const stops = colors
      .map((color, index) => {
        const start = (index / colors.length) * 100;
        const end = ((index + 1) / colors.length) * 100;
        return `${color} ${start}% ${end}%`;
      })
      .join(", ");
    return `linear-gradient(90deg, ${stops})`;
  }
  if (STACK_COLOR[key]) return STACK_COLOR[key];
  return PLATFORMS[key]?.color ?? NODATA;
}

function searchHits(query: string): Profile[] {
  const needle = query.trim().toLowerCase();
  if (!needle) return [];
  const scored: { score: number; profile: Profile }[] = [];
  for (const profile of profiles.values()) {
    const en = profile.name.en.toLowerCase();
    const zh = profile.name["zh-Hant"].toLowerCase();
    const iso = profile.iso.toLowerCase();
    const iso3 = profile.iso3.toLowerCase();
    let score = 0;
    if (iso && iso === needle) score = 100;
    else if (iso3 && iso3 === needle) score = 96;
    else if (en.startsWith(needle) || zh.startsWith(needle)) score = 80;
    else if ((iso && iso.startsWith(needle)) || en.includes(needle) || zh.includes(needle)) score = 50;
    if (!score) continue;
    if (profile.inferred) score -= 4;
    scored.push({ score, profile });
  }
  scored.sort((a, b) => b.score - a.score || a.profile.name.en.localeCompare(b.profile.name.en));
  return scored.slice(0, 8).map((item) => item.profile);
}

function syncUrl() {
  const iso = state.fid && /^[A-Z]{2}$/.test(state.fid) ? state.fid : null;
  const next = serialize({ layer: state.layer, iso, region: state.region, lang: state.lang });
  const current = `${location.search}${location.hash}`;
  if (current !== next) history.replaceState(null, "", next);
}

function pads(): maplibregl.PaddingOptions {
  const mobile = window.innerWidth < 960;
  const open = !panel.hidden;
  // The desktop panel is an in-flow sibling, so the map canvas is already
  // beside it. On a phone the sheet overlays the map, so pad by its height.
  let bottom = 36;
  if (mobile && open) {
    const canvasH = map?.getCanvas().clientHeight ?? window.innerHeight;
    const sheet = panel.getBoundingClientRect().height;
    bottom = Math.min(Math.round(sheet + 12), Math.round(canvasH * 0.58));
  }
  return { top: 36, left: 36, right: 36, bottom };
}

function flyToBBox(bbox: [number, number, number, number], maxZoom: number) {
  if (!map) return;
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  map.fitBounds(
    [
      [bbox[0], bbox[1]],
      [bbox[2], bbox[3]],
    ],
    { padding: pads(), duration: reduce ? 0 : 520, maxZoom },
  );
}

function refit(bbox: [number, number, number, number], maxZoom: number) {
  requestAnimationFrame(() => {
    map?.resize();
    flyToBBox(bbox, maxZoom);
    drawLabels();
  });
}

function setSelected(fid: string | null) {
  if (map?.getSource("countries")) {
    if (selectedId) map.setFeatureState({ source: "countries", id: selectedId }, { selected: false });
    if (fid && geoms.has(fid)) map.setFeatureState({ source: "countries", id: fid }, { selected: true });
  }
  selectedId = fid;
}

function clearCountry() {
  setSelected(null);
  state.fid = null;
  state.sheetExpanded = false;
  panel.classList.remove("expanded");
  panel.hidden = true;
}

function focusWorld() {
  clearCountry();
  state.region = null;
  state.continent = null;
  syncUrl();
  render();
  refit(WORLD_BBOX, 3);
}

function focusContinent(id: string) {
  clearCountry();
  state.continent = id;
  state.region = null;
  syncUrl();
  render();
  const bbox = CONTINENTS[id]?.bbox;
  if (bbox) refit(bbox, 3.8);
}

function focusRegion(id: string) {
  clearCountry();
  state.region = id;
  state.continent = REGIONS[id]?.continent ?? state.continent;
  syncUrl();
  render();
  const bbox = REGIONS[id]?.bbox;
  if (bbox) refit(bbox, 5.2);
}

function selectFid(fid: string) {
  const profile = profiles.get(fid);
  if (!profile) return;
  state.fid = fid;
  if (profile.region) {
    state.region = profile.region;
    state.continent = REGIONS[profile.region]?.continent ?? profile.continent ?? state.continent;
  } else if (profile.continent) {
    state.continent = profile.continent;
  }
  state.sheetExpanded = false;
  panel.classList.remove("expanded");
  panel.hidden = false;
  live.textContent = profile.name[state.lang];
  syncUrl();
  render();
  setSelected(fid);
  const bits = geoms.get(fid);
  if (bits) refit(bits.bbox, 6.5);
  else requestAnimationFrame(() => map?.resize());
  if (window.innerWidth >= 960) panel.focus();
}

function closePanel() {
  if (!state.fid && panel.hidden) return;
  clearCountry();
  syncUrl();
  render();
  requestAnimationFrame(() => map?.resize());
}

function setLayer(layer: LayerId) {
  if (state.layer === layer) return;
  state.layer = layer;
  state.filter = null;
  syncUrl();
  applyPaint();
  applyDim();
  render();
}

function setLang(lang: Lang) {
  if (state.lang === lang) return;
  state.lang = lang;
  localStorage.setItem(LANG_KEY, lang);
  document.documentElement.lang = lang;
  syncUrl();
  render();
  drawLabels();
}

function opacityExpr(layer: LayerId): maplibregl.ExpressionSpecification {
  return [
    "case",
    ["boolean", ["feature-state", "dim"], false],
    0.16,
    ["==", ["get", `m_${layer}`], "nodata"],
    1,
    ["==", ["get", `u_${layer}`], "1"],
    0.68,
    0.92,
  ];
}

function applyPaint() {
  if (!map?.getLayer("countries-fill")) return;
  const layer = state.layer;
  map.setPaintProperty("countries-fill", "fill-color", ["get", `c_${layer}`]);
  map.setPaintProperty("countries-fill", "fill-opacity", opacityExpr(layer));
  if (map.getLayer("countries-pattern")) {
    map.setFilter("countries-pattern", ["!=", ["get", `p_${layer}`], ""]);
    map.setPaintProperty("countries-pattern", "fill-pattern", ["get", `p_${layer}`]);
    map.setPaintProperty("countries-pattern", "fill-opacity", opacityExpr(layer));
  }
}

function applyDim() {
  if (!map?.getSource("countries")) return;
  const layer = state.layer;
  for (const [fid, profile] of profiles) {
    if (!geoms.has(fid)) continue;
    const fill = fillFor(profile, layer);
    let dim = false;
    if (state.filter === "inferred") dim = !profile.inferred;
    else if (state.filter) dim = fill.key !== state.filter;
    map.setFeatureState({ source: "countries", id: fid }, { dim });
  }
}

function ensureChrome() {
  if (!builtLang) {
    builtLang = true;
    for (const lang of ["zh-Hant", "en"] as const) {
      const button = document.createElement("button");
      button.type = "button";
      button.dataset.lang = lang;
      button.textContent = lang === "zh-Hant" ? "繁" : "EN";
      button.addEventListener("click", () => setLang(lang));
      langBox.append(button);
    }
  }
  if (!builtLayers) {
    builtLayers = true;
    for (const layer of LAYERS) {
      const button = document.createElement("button");
      button.type = "button";
      button.dataset.layer = layer;
      button.addEventListener("click", () => setLayer(layer));
      layersEl.append(button);
    }
  }
}

function renderChrome() {
  ensureChrome();
  const lang = state.lang;
  document.title = t(lang, "meta.title");
  document.documentElement.lang = lang;
  mapNode.setAttribute("aria-label", t(lang, "meta.map"));
  skip.textContent = t(lang, "skip.search");
  kicker.textContent = t(lang, "brand.kicker");
  if (lang === "zh-Hant") {
    brandTitle.textContent = t(lang, "brand.zh");
    brandEn.textContent = t(lang, "brand.en");
  } else {
    brandTitle.textContent = t(lang, "brand.en");
    brandEn.textContent = t(lang, "brand.zh");
  }
  yearBadge.textContent = t(lang, "year.badge");
  langBox.setAttribute("aria-label", t(lang, "lang.aria"));
  for (const button of langBox.querySelectorAll("button")) {
    button.setAttribute("aria-pressed", button.dataset.lang === lang ? "true" : "false");
  }
  indexBtn.textContent = t(lang, "panel.index");
  aboutBtn.textContent = t(lang, "about.open");
  aboutRestoreBtn.textContent = t(lang, "about.open");
  hideChromeBtn.textContent = t(lang, "chrome.hide");
  showChromeBtn.textContent = t(lang, "chrome.show");
  hideChromeBtn.setAttribute("aria-pressed", chromeIsHidden() ? "true" : "false");
  layersEl.setAttribute("aria-label", t(lang, "layers.aria"));
  for (const button of layersEl.querySelectorAll("button")) {
    const layer = button.dataset.layer as LayerId;
    button.textContent = t(lang, `layer.${layer}`);
    button.setAttribute("aria-pressed", layer === state.layer ? "true" : "false");
  }
  searchLabel.textContent = t(lang, "search.label");
  searchInput.placeholder = t(lang, "search.placeholder");
  searchInput.setAttribute("aria-label", t(lang, "search.label"));
  const scope = state.region
    ? REGIONS[state.region]?.name[lang]
    : state.continent
      ? CONTINENTS[state.continent]?.name[lang]
      : t(lang, "region.world");
  regionBtn.textContent = `${scope} ▾`;
  regionBtn.setAttribute("aria-label", t(lang, "region.menu"));
  renderRegionMenu();
  renderCrumbs();
  const wide = window.matchMedia("(min-width: 960px)").matches;
  legend.classList.toggle("open", wide || state.legendOpen);
  renderLegend();
  renderPanel();
  if (state.about) renderAbout();
  else about.hidden = true;
  if (state.indexOpen) renderIndex();
  else indexBox.hidden = true;
}

function renderRegionMenu() {
  const lang = state.lang;
  regionPop.replaceChildren();
  const world = document.createElement("button");
  world.type = "button";
  world.textContent = t(lang, "region.world");
  world.addEventListener("click", () => {
    closeRegion();
    focusWorld();
  });
  regionPop.append(world);
  for (const continent of CONTINENT_ORDER) {
    const block = document.createElement("div");
    block.className = "region-block";
    const head = document.createElement("button");
    head.type = "button";
    head.textContent = CONTINENTS[continent]?.name[lang] ?? continent;
    head.addEventListener("click", () => {
      closeRegion();
      focusContinent(continent);
    });
    const sub = document.createElement("div");
    sub.className = "subregions";
    for (const [id, rec] of Object.entries(REGIONS)) {
      if (rec.continent !== continent) continue;
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = rec.name[lang];
      if (state.region === id) button.setAttribute("aria-current", "true");
      button.addEventListener("click", () => {
        closeRegion();
        focusRegion(id);
      });
      sub.append(button);
    }
    block.append(head, sub);
    regionPop.append(block);
  }
}

function renderCrumbs() {
  const lang = state.lang;
  crumbs.setAttribute("aria-label", t(lang, "crumb.aria"));
  crumbs.replaceChildren();
  const parts: { label: string; current: boolean; go?: () => void }[] = [];
  const worldOnly = !state.continent && !state.region && !state.fid;
  parts.push({ label: t(lang, "region.world"), current: worldOnly, go: worldOnly ? undefined : focusWorld });
  if (state.continent) {
    const current = !state.region && !state.fid;
    parts.push({
      label: CONTINENTS[state.continent]?.name[lang] ?? state.continent,
      current,
      go: current ? undefined : () => focusContinent(state.continent as string),
    });
  }
  if (state.region) {
    const current = !state.fid;
    parts.push({
      label: REGIONS[state.region]?.name[lang] ?? state.region,
      current,
      go: current ? undefined : () => focusRegion(state.region as string),
    });
  }
  if (state.fid) {
    const profile = profiles.get(state.fid);
    if (profile) parts.push({ label: profile.name[lang], current: true });
  }
  parts.forEach((part, index) => {
    if (index) {
      const sep = document.createElement("span");
      sep.className = "sep";
      sep.setAttribute("aria-hidden", "true");
      sep.textContent = "/";
      crumbs.append(sep);
    }
    if (part.go && !part.current) {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = part.label;
      button.addEventListener("click", part.go);
      crumbs.append(button);
    } else {
      const span = document.createElement("span");
      span.textContent = part.label;
      if (part.current) span.setAttribute("aria-current", "page");
      crumbs.append(span);
    }
  });
}

function sourceLink(id: string): HTMLAnchorElement | null {
  const source = SOURCES[id];
  if (!source) return null;
  const link = document.createElement("a");
  link.href = source.url;
  link.target = "_blank";
  link.rel = "noopener noreferrer";
  link.textContent = `${source.title} (${source.year})`;
  return link;
}

function inLegendScope(profile: Profile): boolean {
  if (state.region) return profile.region === state.region;
  if (state.continent) return profile.continent === state.continent;
  return true;
}

function legendCounts(): Map<string, number> {
  const counts = new Map<string, number>();
  for (const [fid, profile] of profiles) {
    if (geoms.size && !geoms.has(fid)) continue;
    if (!inLegendScope(profile)) continue;
    const fill = fillFor(profile, state.layer);
    if (fill.mode === "nodata") continue;
    counts.set(fill.key, (counts.get(fill.key) ?? 0) + 1);
  }
  return counts;
}

function renderLegend() {
  const lang = state.lang;
  legend.replaceChildren();
  const head = document.createElement("div");
  head.className = "legend-head";
  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.textContent = t(lang, "legend.toggle");
  toggle.setAttribute("aria-expanded", legend.classList.contains("open") ? "true" : "false");
  toggle.addEventListener("click", () => {
    if (window.matchMedia("(min-width: 960px)").matches) return;
    state.legendOpen = !state.legendOpen;
    legend.classList.toggle("open", state.legendOpen);
    toggle.setAttribute("aria-expanded", state.legendOpen ? "true" : "false");
  });
  head.append(toggle);
  const body = document.createElement("div");
  body.className = "legend-body";
  body.setAttribute("role", "group");
  body.setAttribute("aria-label", t(lang, "legend.aria"));
  const counts = legendCounts();
  const keys = [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
  const pinned = ["nodata", "inferred"];
  for (const [key] of keys) {
    body.append(legendButton(key, false));
  }
  for (const key of pinned) body.append(legendButton(key, key === "inferred"));
  if (state.layer === "social") {
    const note = document.createElement("p");
    note.className = "note";
    note.textContent = t(lang, "legend.social");
    body.append(note);
  }
  if ([...counts.keys()].some((key) => key.includes("+"))) {
    const note = document.createElement("p");
    note.className = "note";
    note.textContent = t(lang, "legend.split");
    body.append(note);
  }
  if (state.filter) {
    const clear = document.createElement("button");
    clear.type = "button";
    clear.className = "all";
    clear.textContent = t(lang, "legend.all");
    clear.addEventListener("click", () => {
      state.filter = null;
      applyDim();
      renderLegend();
    });
    body.append(clear);
  }
  legend.append(head, body);
}

function legendButton(key: string, wash: boolean): HTMLButtonElement {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "row";
  button.setAttribute("aria-pressed", state.filter === key ? "true" : "false");
  const swatch = document.createElement("span");
  swatch.className = wash ? "swatch wash" : "swatch";
  swatch.style.background = swatchBackground(key);
  const label = document.createElement("span");
  label.textContent = swatchLabel(key);
  button.append(swatch, label);
  button.addEventListener("click", () => {
    state.filter = state.filter === key ? null : key;
    applyDim();
    renderLegend();
  });
  return button;
}

function chip(id: string, lang: Lang): HTMLSpanElement {
  const span = document.createElement("span");
  span.className = "chip";
  const dot = document.createElement("i");
  dot.className = "dot";
  dot.style.background = PLATFORMS[id]?.color ?? NODATA;
  span.append(dot, document.createTextNode(platformName(id, lang)));
  return span;
}

function renderPanel() {
  panel.replaceChildren();
  if (!state.fid) {
    panel.hidden = true;
    return;
  }
  const profile = profiles.get(state.fid);
  if (!profile) return;
  const lang = state.lang;
  panel.hidden = false;
  const handle = document.createElement("div");
  handle.className = "handle";
  handle.setAttribute("role", "button");
  handle.tabIndex = 0;
  handle.setAttribute("aria-label", t(lang, "sheet.handle"));
  const body = document.createElement("div");
  body.className = "panel-body";
  const top = document.createElement("div");
  top.className = "panel-top";
  const iso = document.createElement("p");
  iso.className = "iso-line";
  iso.textContent = [profile.iso, profile.iso3].filter(Boolean).join(" · ");
  const close = document.createElement("button");
  close.type = "button";
  close.className = "close-btn";
  close.dataset.close = "1";
  close.textContent = t(lang, "panel.close");
  top.append(iso, close);
  body.append(top);
  if (profile.inferred) {
    const banner = document.createElement("p");
    banner.className = "banner";
    banner.textContent = t(lang, "panel.inferred");
    body.append(banner);
  }
  const title = document.createElement("h2");
  title.id = "panel-title";
  title.textContent = profile.name[lang];
  body.append(title);
  const meta = document.createElement("div");
  meta.className = "meta";
  const badge = document.createElement("span");
  badge.className = "badge";
  const dot = document.createElement("i");
  dot.className = "dot";
  dot.style.background = STACK_COLOR[profile.stack] ?? NODATA;
  badge.append(dot, document.createTextNode(t(lang, `stack.${profile.stack}`)));
  const conf = document.createElement("span");
  conf.className = "conf";
  conf.textContent = t(lang, `conf.${profile.confidence}`);
  const year = document.createElement("span");
  year.className = "year-mini";
  year.textContent = String(profile.year);
  meta.append(badge, conf, year);
  body.append(meta);
  const lifeHead = document.createElement("h3");
  lifeHead.textContent = t(lang, "panel.life");
  body.append(lifeHead);
  const life = document.createElement("div");
  life.className = "life";
  for (const cat of CATS) {
    const cell = profile[cat];
    const block = document.createElement("section");
    block.className = cat === state.layer ? "cat current" : "cat";
    block.dataset.cat = cat;
    const label = document.createElement("div");
    label.className = "cat-label";
    const yearBit = cell.year && cell.year !== profile.year ? ` · ${cell.year}` : "";
    label.textContent = `${t(lang, `cat.${cat}`)}${yearBit}`;
    block.append(label);
    if (!cell.dominant.length) {
      const empty = document.createElement("p");
      empty.className = "muted";
      empty.textContent = t(lang, "panel.noLeader");
      block.append(empty);
    } else {
      const chips = document.createElement("div");
      chips.className = "chips";
      for (const id of cell.dominant) chips.append(chip(id, lang));
      block.append(chips);
    }
    if (cell.secondary.length) {
      const secondary = document.createElement("p");
      secondary.className = "secondary";
      secondary.textContent = `${t(lang, "panel.secondary")}: ${cell.secondary
        .map((id) => platformName(id, lang))
        .join(" · ")}`;
      block.append(secondary);
    }
    if (cell.notes[lang]) {
      const note = document.createElement("p");
      note.className = "cat-note";
      note.textContent = cell.notes[lang];
      block.append(note);
    }
    life.append(block);
  }
  body.append(life);
  const notesHead = document.createElement("h3");
  notesHead.textContent = t(lang, "panel.notes");
  const notes = document.createElement("p");
  notes.className = "country-note";
  notes.textContent = profile.notes[lang];
  body.append(notesHead, notes);
  const srcHead = document.createElement("h3");
  srcHead.textContent = t(lang, "panel.sources");
  body.append(srcHead);
  const ids = sourceList(profile);
  if (!ids.length) {
    const none = document.createElement("p");
    none.className = "muted";
    none.textContent = t(lang, "panel.noSource");
    body.append(none);
  } else {
    const list = document.createElement("div");
    list.className = "sources";
    for (const id of ids) {
      const source = SOURCES[id];
      if (!source) continue;
      const link = document.createElement("a");
      link.href = source.url;
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = `${source.title} (${source.year})`;
      list.append(link);
    }
    body.append(list);
  }
  panel.append(handle, body);
  scrollActiveCat();
}

function scrollActiveCat() {
  if (!CATS.includes(state.layer as (typeof CATS)[number])) return;
  requestAnimationFrame(() => {
    const block = panel.querySelector<HTMLElement>(`[data-cat="${state.layer}"]`);
    if (!block) return;
    const delta = block.getBoundingClientRect().top - panel.getBoundingClientRect().top;
    panel.scrollTop += delta - 8;
  });
}

function renderAbout() {
  const lang = state.lang;
  about.replaceChildren();
  const card = document.createElement("div");
  card.className = "dialog";
  card.setAttribute("role", "dialog");
  card.setAttribute("aria-modal", "true");
  const close = document.createElement("button");
  close.type = "button";
  close.className = "close-btn";
  close.textContent = t(lang, "about.close");
  close.addEventListener("click", closeAbout);
  const title = document.createElement("h2");
  title.id = "about-title";
  title.textContent = t(lang, "about.title");
  card.setAttribute("aria-labelledby", "about-title");
  const qual = document.createElement("p");
  qual.className = "about-qual";
  qual.textContent = t(lang, "footer.qual");
  card.append(close, title, qual);
  for (let i = 1; i <= 10; i++) {
    const paragraph = document.createElement("p");
    paragraph.textContent = t(lang, `about.p${i}`);
    card.append(paragraph);
  }
  const cite = document.createElement("section");
  cite.className = "cite";
  const sourcesHead = document.createElement("h3");
  sourcesHead.textContent = t(lang, "about.sources");
  cite.append(sourcesHead);
  for (const layer of LAYERS) {
    const row = document.createElement("div");
    row.className = "cite-row";
    if (layer === state.layer) {
      row.classList.add("current");
      row.setAttribute("aria-current", "true");
    }
    const label = document.createElement("p");
    label.className = "cat-label";
    label.textContent =
      layer === state.layer
        ? `${t(lang, `layer.${layer}`)} · ${t(lang, "about.current")}`
        : t(lang, `layer.${layer}`);
    const links = document.createElement("div");
    links.className = "sources";
    for (const id of LAYER_SOURCE_IDS[layer] ?? []) {
      const link = sourceLink(id);
      if (link) links.append(link);
    }
    row.append(label, links);
    cite.append(row);
  }
  const credit = document.createElement("p");
  credit.className = "about-credit";
  credit.textContent = t(lang, "footer.ne");
  cite.append(credit);
  card.append(cite);
  about.append(card);
  about.hidden = false;
}

function profilesInScope(): Profile[] {
  const list = [...profiles.values()].filter((profile) => {
    if (state.region) return profile.region === state.region;
    if (state.continent) return profile.continent === state.continent;
    return true;
  });
  list.sort((a, b) => a.name[state.lang].localeCompare(b.name[state.lang], state.lang));
  return list;
}

function renderIndex() {
  const lang = state.lang;
  indexBox.replaceChildren();
  const card = document.createElement("div");
  card.className = "dialog";
  card.setAttribute("role", "dialog");
  card.setAttribute("aria-modal", "true");
  const close = document.createElement("button");
  close.type = "button";
  close.className = "close-btn";
  close.textContent = t(lang, "index.close");
  close.addEventListener("click", closeIndex);
  const title = document.createElement("h2");
  title.id = "index-title";
  title.textContent = t(lang, "index.title");
  card.setAttribute("aria-labelledby", "index-title");
  const intro = document.createElement("p");
  intro.textContent = t(lang, "index.intro");
  card.append(close, title, intro);
  const groups = new Map<string, Profile[]>();
  for (const profile of profilesInScope()) {
    const key = profile.region || profile.continent || "—";
    const bucket = groups.get(key) ?? [];
    bucket.push(profile);
    groups.set(key, bucket);
  }
  if (!groups.size) {
    const empty = document.createElement("p");
    empty.textContent = t(lang, "index.empty");
    card.append(empty);
  }
  for (const [key, bucket] of groups) {
    const group = document.createElement("section");
    group.className = "group";
    const heading = document.createElement("h3");
    heading.textContent = REGIONS[key]?.name[lang] ?? CONTINENTS[key]?.name[lang] ?? key;
    group.append(heading);
    for (const profile of bucket) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "index-row";
      const name = document.createElement("span");
      name.textContent = profile.name[lang];
      const extra = document.createElement("span");
      extra.textContent = profile.inferred ? t(lang, "index.tag") : profile.iso;
      if (profile.inferred) extra.className = "tag";
      else extra.className = "iso-line";
      button.append(name, extra);
      button.addEventListener("click", () => {
        closeIndex();
        selectFid(profile.fid);
      });
      group.append(button);
    }
    card.append(group);
  }
  indexBox.append(card);
  indexBox.hidden = false;
}

function openAbout(opener?: HTMLElement) {
  aboutOpener = opener ?? aboutBtn;
  state.about = true;
  renderAbout();
  about.querySelector("button")?.focus();
}

function closeAbout() {
  state.about = false;
  about.hidden = true;
  about.replaceChildren();
  if (focusIfShown(aboutOpener)) return;
  if (chromeIsHidden()) focusIfShown(aboutRestoreBtn) || focusIfShown(showChromeBtn);
  else focusIfShown(aboutBtn) || focusIfShown(hideChromeBtn);
}

function openIndex() {
  state.indexOpen = true;
  renderIndex();
  indexBox.querySelector("button")?.focus();
}

function closeIndex() {
  state.indexOpen = false;
  indexBox.hidden = true;
  indexBox.replaceChildren();
}

function closeRegion() {
  regionPop.hidden = true;
  regionBtn.setAttribute("aria-expanded", "false");
}

function toggleRegion() {
  const open = regionPop.hidden;
  regionPop.hidden = !open;
  regionBtn.setAttribute("aria-expanded", open ? "true" : "false");
}

function hideResults() {
  results.hidden = true;
  results.replaceChildren();
  searchInput.setAttribute("aria-expanded", "false");
  searchActive = 0;
}

function showResults(hits: Profile[]) {
  results.replaceChildren();
  if (!searchInput.value.trim()) {
    hideResults();
    return;
  }
  results.hidden = false;
  searchInput.setAttribute("aria-expanded", "true");
  if (!hits.length) {
    const empty = document.createElement("li");
    empty.className = "empty";
    empty.textContent = t(state.lang, "search.empty");
    results.append(empty);
    return;
  }
  hits.forEach((profile, index) => {
    const item = document.createElement("li");
    item.dataset.fid = profile.fid;
    item.setAttribute("role", "option");
    item.setAttribute("aria-selected", index === searchActive ? "true" : "false");
    if (index === searchActive) item.classList.add("active");
    const name = document.createElement("span");
    name.textContent = profile.name[state.lang];
    const iso = document.createElement("span");
    iso.className = "iso";
    iso.textContent = profile.iso || profile.iso3 || "";
    item.append(name, iso);
    results.append(item);
  });
}

function showTip(point: maplibregl.Point, fid: string) {
  const profile = profiles.get(fid);
  if (!profile || !map) return;
  const fill = fillFor(profile, state.layer);
  tip.replaceChildren();
  const strong = document.createElement("strong");
  strong.textContent = profile.name[state.lang];
  const lead = document.createElement("span");
  if (fill.mode === "nodata") lead.textContent = t(state.lang, "tip.nodata");
  else if (fill.mode === "split") {
    lead.textContent = `${fill.ids.map((id) => nameOf(id, state.layer, state.lang)).join(" · ")} · ${t(state.lang, "tip.contested")}`;
  } else {
    lead.textContent = fill.ids.map((id) => nameOf(id, state.layer, state.lang)).join(" · ");
  }
  tip.append(strong, lead);
  if (profile.inferred) {
    const mark = document.createElement("span");
    mark.textContent = t(state.lang, "tip.inferred");
    tip.append(mark);
  }
  const rect = map.getContainer().getBoundingClientRect();
  const left = Math.min(rect.left + point.x + 14, window.innerWidth - 280);
  const top = Math.min(rect.top + point.y + 14, window.innerHeight - 90);
  tip.style.left = `${Math.max(8, left)}px`;
  tip.style.top = `${Math.max(8, top)}px`;
  tip.hidden = false;
}

function drawLabels() {
  if (!labelLayer || !map) return;
  labelLayer.replaceChildren();
  const zoom = map.getZoom();
  const regionMode = !!state.region;
  if (!regionMode && zoom < 4.6) return;
  const bounds = map.getBounds();
  const placed: { x: number; y: number }[] = [];
  let shown = 0;
  for (const [fid, geom] of geoms) {
    const profile = profiles.get(fid);
    if (!profile) continue;
    if (regionMode && profile.region !== state.region) continue;
    if (!bounds.contains(geom.label as [number, number])) continue;
    if (!regionMode && shown > 36) break;
    const point = map.project(geom.label as [number, number]);
    if (placed.some((item) => Math.hypot(item.x - point.x, item.y - point.y) < 54)) continue;
    placed.push(point);
    shown += 1;
    const span = document.createElement("span");
    span.className = "map-label";
    span.textContent = profile.name[state.lang];
    span.style.left = `${point.x}px`;
    span.style.top = `${point.y}px`;
    labelLayer.append(span);
  }
}

function render() {
  renderChrome();
  drawLabels();
}

function bindMap(collection: GeoCollection, patterns: string[]) {
  map = new maplibregl.Map({
    container: mapNode,
    style: {
      version: 8,
      sources: {
        graticule: { type: "geojson", data: graticule() },
        countries: { type: "geojson", data: collection as never },
      },
      layers: [
        { id: "bg", type: "background", paint: { "background-color": "#d9e2dc" } },
        {
          id: "graticule",
          type: "line",
          source: "graticule",
          paint: { "line-color": "#c5d0c9", "line-width": 0.6, "line-opacity": 0.8 },
        },
        {
          id: "countries-fill",
          type: "fill",
          source: "countries",
          paint: {
            "fill-color": ["get", `c_${state.layer}`],
            "fill-opacity": opacityExpr(state.layer),
          },
        },
        {
          id: "countries-halo",
          type: "line",
          source: "countries",
          paint: {
            "line-color": "#f7f3eb",
            "line-width": ["case", ["boolean", ["feature-state", "selected"], false], 4.4, 0],
            "line-opacity": 0.95,
          },
        },
        {
          id: "countries-line",
          type: "line",
          source: "countries",
          paint: {
            "line-color": "#1c1712",
            "line-width": [
              "case",
              ["boolean", ["feature-state", "selected"], false],
              2,
              ["boolean", ["feature-state", "hover"], false],
              1.25,
              0.45,
            ],
            "line-opacity": [
              "case",
              ["boolean", ["feature-state", "selected"], false],
              0.95,
              ["boolean", ["feature-state", "hover"], false],
              0.75,
              0.38,
            ],
          },
        },
      ],
    },
    center: [18, 18],
    zoom: 1.3,
    minZoom: 0.85,
    maxZoom: 8,
    attributionControl: false,
    fadeDuration: 0,
  });
  map.addControl(
    new maplibregl.NavigationControl({ showCompass: false, visualizePitch: false }),
    "top-left",
  );
  map.addControl(
    new maplibregl.AttributionControl({ compact: true, customAttribution: "Natural Earth" }),
    "bottom-right",
  );
  map.dragRotate.disable();
  map.touchZoomRotate.disableRotation();
  map.doubleClickZoom.disable();

  map.on("load", () => {
    if (!map) return;
    for (const id of patterns) ensurePattern(map, id);
    map.addLayer(
      {
        id: "countries-pattern",
        type: "fill",
        source: "countries",
        filter: ["!=", ["get", `p_${state.layer}`], ""],
        paint: {
          "fill-pattern": ["get", `p_${state.layer}`],
          "fill-opacity": opacityExpr(state.layer),
        },
      },
      "countries-halo",
    );
    labelLayer = document.createElement("div");
    labelLayer.className = "labels";
    map.getContainer().append(labelLayer);
    applyPaint();
    applyDim();
    applyEntry();
  });

  const hitLayers = () =>
    ["countries-pattern", "countries-fill"].filter((id) => map?.getLayer(id));

  const countryAt = (point: maplibregl.Point) => {
    if (!map?.isStyleLoaded()) return "";
    const features = map.queryRenderedFeatures(point, { layers: hitLayers() });
    const feature = features[0];
    if (!feature) return "";
    return String(feature.id ?? feature.properties?.fid ?? "");
  };

  map.on("mousemove", (event) => {
    if (!map) return;
    const coarse = window.matchMedia("(hover: none), (max-width: 959px)").matches;
    const fid = coarse ? "" : countryAt(event.point);
    if (hoverId && hoverId !== fid) map.setFeatureState({ source: "countries", id: hoverId }, { hover: false });
    hoverId = fid || null;
    if (!fid) {
      tip.hidden = true;
      map.getCanvas().style.cursor = "";
      return;
    }
    map.setFeatureState({ source: "countries", id: fid }, { hover: true });
    map.getCanvas().style.cursor = "pointer";
    showTip(event.point, fid);
  });
  map.on("mouseout", () => {
    if (map && hoverId) map.setFeatureState({ source: "countries", id: hoverId }, { hover: false });
    hoverId = null;
    tip.hidden = true;
    if (map) map.getCanvas().style.cursor = "";
  });
  map.on("click", (event) => {
    const fid = countryAt(event.point);
    if (!fid || !profiles.has(fid)) return;
    const mobile = window.matchMedia("(max-width: 959px)").matches;
    if (mobile && state.fid === fid) {
      closePanel();
      return;
    }
    selectFid(fid);
  });
  map.on("move", () => drawLabels());
}

function applyEntry() {
  const parsed = parseView(location.search);
  if (parsed.iso && (profiles.has(parsed.iso) || profileByIso(parsed.iso))) {
    const fid = profiles.has(parsed.iso) ? parsed.iso : profileByIso(parsed.iso)?.fid;
    if (fid && profiles.has(fid)) {
      selectFid(fid);
      return;
    }
  }
  if (parsed.region && REGIONS[parsed.region]) {
    focusRegion(parsed.region);
    return;
  }
  focusWorld();
}

async function loadGeo() {
  const url = `${import.meta.env.BASE_URL}geo/countries.geojson`;
  const response = await fetch(url);
  if (!response.ok) throw new Error(String(response.status));
  const collection = (await response.json()) as GeoCollection;
  const joined = joinCountries(collection, profiles);
  geoms = joined.geoms;
  bindMap(collection, joined.patterns);
}

function onKeydown(event: KeyboardEvent) {
  const target = event.target as HTMLElement | null;
  const typing = !!target && (target.tagName === "INPUT" || target.tagName === "TEXTAREA");
  if (event.key === "/" && !typing && !event.metaKey && !event.ctrlKey && !event.altKey) {
    event.preventDefault();
    if (chromeIsHidden()) setHideChrome(false, "search");
    else {
      searchInput.focus();
      searchInput.select();
    }
    return;
  }
  if (event.key !== "Escape") return;
  if (!about.hidden) {
    closeAbout();
    return;
  }
  if (!indexBox.hidden) {
    closeIndex();
    return;
  }
  if (!regionPop.hidden) {
    closeRegion();
    return;
  }
  if (!results.hidden) {
    hideResults();
    return;
  }
  if (!panel.hidden) {
    closePanel();
    return;
  }
  if (state.filter) {
    state.filter = null;
    applyDim();
    renderLegend();
  }
}

function boot() {
  const parsed = parseView(location.search);
  const storage = chromeStorage();
  state.lang = resolveLang(location.search, storage?.getItem(LANG_KEY) ?? null);
  state.layer = parsed.layer;
  state.region = parsed.region;
  if (parsed.region) state.continent = REGIONS[parsed.region]?.continent ?? null;
  hideChromePref = readHideChrome(storage);
  syncChromeClass();
  try {
    storage?.setItem(LANG_KEY, state.lang);
  } catch {
    /* private mode */
  }
  render();

  aboutBtn.addEventListener("click", () => openAbout(aboutBtn));
  aboutRestoreBtn.addEventListener("click", () => openAbout(aboutRestoreBtn));
  hideChromeBtn.addEventListener("click", () => setHideChrome(true, "toggle"));
  showChromeBtn.addEventListener("click", () => setHideChrome(false, "toggle"));
  skip.addEventListener("click", (event) => {
    if (!chromeIsHidden()) return;
    event.preventDefault();
    setHideChrome(false, "search");
  });
  indexBtn.addEventListener("click", openIndex);
  regionBtn.addEventListener("click", toggleRegion);
  about.addEventListener("click", (event) => {
    if (event.target === about) closeAbout();
  });
  indexBox.addEventListener("click", (event) => {
    if (event.target === indexBox) closeIndex();
  });
  searchWrap.addEventListener("click", (event) => event.stopPropagation());
  regionWrap.addEventListener("click", (event) => event.stopPropagation());
  document.addEventListener("click", () => {
    closeRegion();
    hideResults();
  });
  document.addEventListener("keydown", onKeydown);
  searchInput.addEventListener("input", () => {
    searchActive = 0;
    showResults(searchHits(searchInput.value));
  });
  searchInput.addEventListener("keydown", (event) => {
    const items = [...results.querySelectorAll<HTMLElement>("[data-fid]")];
    if (event.key === "ArrowDown" && items.length) {
      event.preventDefault();
      searchActive = Math.min(items.length - 1, searchActive + 1);
      showResults(searchHits(searchInput.value));
    } else if (event.key === "ArrowUp" && items.length) {
      event.preventDefault();
      searchActive = Math.max(0, searchActive - 1);
      showResults(searchHits(searchInput.value));
    } else if (event.key === "Enter") {
      event.preventDefault();
      const fid = items[searchActive]?.dataset.fid ?? items[0]?.dataset.fid;
      if (fid) {
        hideResults();
        searchInput.blur();
        selectFid(fid);
      }
    } else if (event.key === "Escape") {
      event.stopPropagation();
      if (searchInput.value || !results.hidden) {
        searchInput.value = "";
        hideResults();
        return;
      }
      closePanel();
    }
  });
  results.addEventListener("click", (event) => {
    const item = (event.target as HTMLElement).closest<HTMLElement>("[data-fid]");
    if (!item?.dataset.fid) return;
    hideResults();
    selectFid(item.dataset.fid);
  });
  panel.addEventListener("click", (event) => {
    const target = event.target as HTMLElement;
    if (target.closest("[data-close]")) closePanel();
  });
  panel.addEventListener("pointerdown", (event) => {
    const target = event.target as HTMLElement;
    if (!target.closest(".handle")) return;
    const startY = event.clientY;
    const up = (ev: PointerEvent) => {
      const dy = ev.clientY - startY;
      if (dy > 72) closePanel();
      else if (dy < -36) {
        state.sheetExpanded = true;
        panel.classList.add("expanded");
        map?.resize();
      } else if (state.sheetExpanded && dy > 28) {
        state.sheetExpanded = false;
        panel.classList.remove("expanded");
        map?.resize();
      }
      window.removeEventListener("pointerup", up);
    };
    window.addEventListener("pointerup", up);
  });
  window.addEventListener("resize", () => {
    resizeMapSoon();
    const wide = window.matchMedia("(min-width: 960px)").matches;
    legend.classList.toggle("open", wide || state.legendOpen);
    if (chromeIsHidden()) hideChromeBtn.setAttribute("aria-pressed", "true");
    else hideChromeBtn.setAttribute("aria-pressed", "false");
    drawLabels();
  });

  loadGeo().catch(() => {
    geoFail.hidden = false;
    geoFail.textContent = t(state.lang, "geo.fail");
    applyEntry();
  });
}

boot();
