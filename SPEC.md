# SPEC — Internet Nations / 互聯網民族

Compiled 2026-11-22 (Asia/Shanghai). Research and product brief for v1. Implementation should follow this file and the datasets in `data/`. Do not invent precise percentages. Do not add a backend.

## 1. Product

A static, bilingual, editorial interactive world map of **internet nations** — the platform “life circles” of netizens, analogous to language-distribution maps, not a generic dashboard choropleth.

Users should be able to:

- Pan and zoom the world, then zoom to a **continent** and a **region** (e.g. East Asia, Western Europe, Southeast Asia, Latin America).
- Switch **layers**: Overview (which stack dominates), Social, Messaging, Payments, Search, AI.
- Search / jump to a country.
- Click or tap a country to open a **side panel** (desktop) or **bottom sheet** (phone) showing that country’s internet life circle across all five categories, with year badge, confidence, notes, and source links.
- Deep-link and share a view: `?layer=payments&iso=JP&region=east-asia&lang=zh-Hant` (hash or query both acceptable; prefer query). Persist language preference in `localStorage`.
- Instantly toggle Traditional Chinese (default, Hong Kong) and English.

v1 is static. All data is in-repo. No paid Mapbox token. No claim of UAT or acceptance.

## 2. Taxonomy

### 2.1 Layers (dimensions)

| id | zh-Hant | en | What is mapped |
|---|---|---|---|
| `overview` | 總覽 | Overview | Dominant **stack** (internet-nation tribe), not a single app |
| `social` | 社交 | Social | Everyday social / community feed (not including pure messaging unless that is the local social fabric) |
| `messaging` | 通訊 | Messaging | Default chat app for friends/family/business |
| `payments` | 支付 | Payments | Everyday retail / P2P / transit wallets, not just credit-card brands |
| `search` | 搜尋 | Search | Default web search engine |
| `ai` | AI | AI | Consumer AI assistant / chatbot, where public data exists |

YouTube is almost universal as video. Treat it as a **persistent secondary** in Social unless it is clearly the distinctive local “town square”. Do not colour the social layer as “YouTube everywhere”.

### 2.2 Overview stacks (internet nations)

Use these ids in `countries.json` `stack` and in the Overview legend:

| id | zh-Hant | en | Typical members |
|---|---|---|---|
| `wechat-superapp` | 微信超級應用圈 | WeChat Super-App | Mainland China |
| `line-sphere` | LINE 圈 | LINE Sphere | Japan, Taiwan, Thailand |
| `kakao-naver` | Kakao／Naver 圈 | Kakao–Naver | South Korea |
| `zalo-hybrid` | Zalo 混合圈 | Zalo Hybrid | Vietnam (Zalo chat + Meta/TikTok social + Google search) |
| `vk-yandex` | VK／Yandex 圈 | VK–Yandex | Russia; Belarus tentatively |
| `whatsapp-meta` | WhatsApp／Meta 圈 | WhatsApp–Meta | Most of Latin America, Africa, South Asia, much of Europe and SEA |
| `anglosphere-mixed` | 英語圈混合 | Anglosphere Mixed | US, Canada, Australia, New Zealand, Ireland — iMessage + Messenger/WhatsApp, Google, cards/Apple Pay, Meta social |
| `unknown` | 資料不足 | Data-poor | Use only when even a regional inference would be misleading |

A country can have a distinctive **payment rail** (Pix, UPI, M-Pesa, Swish, PromptPay, PayNow) while still belonging to `whatsapp-meta`. Show that in the Payments layer and in the country panel; do not invent a new overview stack for every rail.

### 2.3 Platform ids

Canonical ids live in `data/platforms.json`. Country rows reference those ids only. If a local app is important but not in the palette, add it there first (name en + zh-Hant, category, colour).

### 2.4 Country record shape

Every country in `data/countries.json` must have:

- `iso` (ISO 3166-1 alpha-2), `iso3`, bilingual `name`
- `continent`, `region` (ids from `data/regions.json`)
- `stack` (overview)
- `year` (best year of the evidence, often 2025–2026; may differ by category — if so, put category years in notes)
- `confidence`: `high` | `medium` | `low`
- For each of `social`, `messaging`, `payments`, `search`, `ai`:
  - `dominant`: array of platform ids (1–3, ordered)
  - `secondary`: array of platform ids
  - `notes`: short bilingual or language-keyed string; caveats, disagreements, transit-vs-retail splits
  - `sources`: array of source ids from `data/sources.json`
  - `year` optional override
- `notes` at country level for the life-circle story
- Never invent precise percentages. If two sources disagree (Korea search, US messaging), say so in `notes` and keep `confidence` honest.

Countries not given a full profile may be filled from `data/regional-defaults.json` at build time, but the UI must label them **資料不足／區域推斷** (data-poor / regional inference) and must not look as certain as a high-confidence profile.

## 3. Layout and UX (borrowed from sites actually studied)

These are layout rules to implement, not a visual clone. Do not copy logos, unique illustrations, or trademarked wordmarks.

### 3.1 Our World in Data (Grapher map views) — primary structure

Studied: [owid redesign](https://ourworldindata.org/redesigning-our-interactive-data-visualizations), Grapher `map.region` (World / continents), [observed typography/colour](https://styleguide.fyi/sites/ourworldindata.org), source footers in the Grapher schema.

Borrow:

- The **map is the product**. Chrome is thin. No marketing hero above the fold.
- **Region focus control** (World, continents, then our finer regions) in the upper-right cluster, like OWID’s map region menu.
- **Click a country → persistent detail**, not a modal that eats the map. OWID jumps to a country chart; we open a side panel and keep the map.
- **Source footer always visible**: dataset name, year, “learn more / sources” link. Year badge near the title.
- **No-data** is a first-class legend swatch (light grey), never a missing country shaped like a bug.
- On narrow screens, controls and the legend stack; the ranked/detail surface moves under or into a sheet. Touch targets ≥ 44px.
- Deep-linkable view state (layer, entity, region, language).

Do **not** clone OWID’s Lato + Playfair + navy brand. We are an atlas of platform tribes, not a development-stats institute.

### 3.2 Language-distribution / ethnographic maps (Ethnologue-style, Glottolog, Native Land)

Studied: [Native Land](https://native-land.ca/) and reviews noting overlap/visual overload; language-family choropleths generally.

Borrow:

- **Categorical colour** by tribe/platform, not a sequential “more/less” scale. This is a language map, not a GDP map.
- A **search box that flies to a place**, plus **layer toggles**.
- Hover = short tooltip (name + current-layer leader). Click = a focused **detail card / panel**, not competing popups.
- Avoid Native Land’s main failure: too many overlapping fills and labels at once. One layer at a time. Labels appear at region zoom, not a global name collision.
- Breadcrumb orientation: **World → Continent → Region → Country**.

### 3.3 The True Size, WHO / World Bank explorers, MapLibre showcases

Borrow:

- Honest projection/scale: use a standard web mercator for interaction (MapLibre), but never pretend land area is the story. The story is platforms. A short “about this map” note can mention mercator distortion.
- World Bank / WHO: serious typography, visible vintage (year), citation, a calm legend, a way back to the world view.
- MapLibre showcase quality: smooth flyTo, no tile flash, no default “streets” basemap competing with fills. Coastlines and a faint graticule or oceanic texture only.

### 3.4 Concrete layout (desktop, ≥ 960px)

```
┌─ top bar ──────────────────────────────────────────────────────────┐
│ Wordmark 互聯網民族 / Internet Nations    year badge    繁｜EN     │
│ Layer pills: 總覽 社交 通訊 支付 搜尋 AI     search     region ▾  │
│ Breadcrumb: 世界 / 亞洲 / 東亞                                      │
└────────────────────────────────────────────────────────────────────┘
┌─ map (full remaining viewport) ──────────────┬─ side panel (0–400px)─┐
│  countries filled by current layer           │ Country name          │
│  tooltip on hover                            │ Stack badge + conf.   │
│  [+][−] zoom, maybe locate                   │ Life circle: 5 rows   │
│                                              │ Notes                 │
│  legend (bottom-left, categorical)           │ Sources (links)       │
└──────────────────────────────────────────────┴───────────────────────┘
┌─ footer: sources for this layer · methodology · © citations ─────────┐
```

- Side panel is closed until a country is selected; the map is full-bleed. Opening it should not jump the camera off the country (pad the bounds).
- Legend filters (optional v1 stretch): clicking a swatch can dim other platforms. If implemented, it must be reversible and keyboard-accessible.
- Keyboard: `/` or the search field focuses search; Esc closes panel; arrows not required for map pan (pointer + buttons are enough).

### 3.5 Mobile (< 960px)

- Top bar compresses: wordmark, layer select (scrollable pills or a compact select), language, search icon.
- Region control inside a “Explore” menu or under the layer pills.
- Country detail is a **bottom sheet** (drag to expand, swipe down to close), not a full-screen takeover that loses the map.
- Legend is compact, collapsible, above the footer or inside the sheet.
- No hover; a light tap on a country opens the sheet. A second tap on the same country may close it.

### 3.6 Visual direction

Editorial atlas, first-class, closer to a printed language map or a Ticket-Sweeper/OWID level of polish than to a Bootstrap admin or a student D3 choropleth.

Suggested tokens (implementer may refine, but stay in this family):

- Background / ocean: warm paper or deep ink-blue-black. Prefer **warm paper** `#f3eee4` with ocean `#d9e2dc` and ink `#1c1712` for credibility and CJK sharpness; a dark theme is an optional toggle, not required in v1.
- Type: a distinctive **display serif** for the wordmark and country titles (e.g. Fraunces or Instrument Serif) + **Noto Sans TC** (or Noto Sans HK) for all UI and body, + a **tabular mono** (IBM Plex Mono) for ISO codes and years.
- Platform colours: a hand-tuned categorical palette in `platforms.json`, colour-blind safer (no red/green-only pairs for opposing platforms). Stacks get the colour of their defining platform.
- Selection: a bright hairline + slight raise, not a thick neon stroke.
- Motion: 300–600ms flyTo, no bounce, no confetti.

## 4. Interaction details

- **Overview layer**: fill by `stack`. Legend shows the eight stacks (hide `unknown` if unused, always show data-poor grey).
- **Other layers**: fill by the first `dominant` platform id in that category. If two platforms are a true duopoly (Alipay + WeChat Pay; Naver vs Google), use a **hatched / split** fill or a dedicated “duopoly” colour and explain in the legend — do not silently pick a winner when notes say the lead is contested.
- **Zoom presets** (must ship): World; six continents; all regions in `data/regions.json` with `bbox`. Buttons or a two-level menu are fine. Programmatic `fitBounds` with padding for the panel.
- **Search**: type-ahead on en + zh-Hant names and ISO2/ISO3. Enter or click flies to the country and opens the panel.
- **i18n**: all chrome, legend titles, stack names, category labels, confidence labels, empty states, footer. Platform names may stay in native/English form where that is how they are known (WhatsApp, 微信, 八達通) but need a zh-Hant label in `platforms.json`.
- **Citations**: every panel lists the source titles and URLs used for that country. Footer lists the layer’s primary sources. Link out with `rel="noopener noreferrer"`.
- **About / methodology**: a short overlay or `/#about` drawer summarising DATA.md (no need for a separate multipage site).

## 5. Technical constraints

- Path: this repo, Vite + TypeScript.
- Map: **MapLibre GL**. Basemap: a free style (OpenFreeMap / a local minimal style) **or** no raster basemap — just Natural Earth (or equivalent public) country polygons. Preferred geo: Natural Earth 50m (or 110m plus 50m for closer zooms). Public domain / public data only.
- Package manager: **bun**. Scripts: `bun install`, `bun run dev`, `bun run build`, `bun test` (or `bun run check`). All must be green.
- Tests (self-check, must exist):
  - Dataset schema: unique ISO, every country has required fields, every platform id and source id resolves, every region has a bbox.
  - Deep-link parse/serialize for `layer`, `iso`, `region`, `lang`.
  - i18n: no missing keys for `zh-Hant` and `en`.
- Accessibility: focus states, contrast on labels, map has a text alternative (search + country list in the panel or a “countries in this region” list).
- Performance: first load must stay reasonable; simplify or pre-simplify geo; do not ship a 20 MB raw GeoJSON if a quantized/topojson or a simplified 50m file will do.
- Deploy target: Cloudflare Pages static `dist/`. Do not hard-code a stale host in OG tags if you add them; a relative or documented production host is fine.
- Do **not** commit secrets. Do **not** merge to `main`. Work on the current feature branch.

## 6. Out of scope for v1

Subnational maps (provinces, cities), time sliders, user accounts, live API polling, precise percent labels, app-store or e-commerce as first-class layers (may appear in notes), 3D globe, paying for Mapbox.

## 7. Definition of done

- Beautiful bilingual map, desktop and phone, with layer switch, region zoom, search, country panel, legend, sources, year badge, deep links.
- `bun test` / check and `bun run build` green.
- README explains how to run locally and what the data is (and is not).
