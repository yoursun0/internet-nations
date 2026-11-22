# Internet Nations / 互聯網民族

A bilingual editorial atlas of how people actually live online: social, messaging, payments, search, and AI, by country and region.

The map is the product. Traditional Chinese (Hong Kong) is the default; English is one toggle away. The choice is kept in `localStorage` and in the query string.

## Run locally

```bash
bun install
bun run dev
bun test
bun run build
```

`bun run dev` starts Vite. `bun test` checks the dataset, deep links, the contested-fill rules, and that every interface string exists in both languages. `bun run check` is the typecheck plus those tests. `bun run build` typechecks and writes `dist/`.

There is no backend and no Mapbox token. Country shapes are Natural Earth 50m admin-0, public domain, simplified and stored at `public/geo/countries.geojson`. The ocean is a flat atlas colour, not a street basemap.

## What the data is

A qualitative, cited atlas. Each full profile in `data/countries.json` names dominant and secondary platforms, a year, a confidence, notes, and source ids. It is **not** a market-share spreadsheet. Precise percentages are omitted on purpose.

Method, caveats, and the source list are in [DATA.md](DATA.md). Product rules, taxonomy, and layout are in [SPEC.md](SPEC.md).

A few leads are drawn as stripes because the sources do not support a single winner:

- South Korea search (Naver and Google)
- Alipay and WeChat Pay
- Messaging in the United States, Canada, Australia, Ireland, and New Zealand, where Android panels miss iMessage

Mainland China, Hong Kong, Macao, and Russia are not coloured as ChatGPT defaults. OpenAI’s supported-country list does not include them. See DATA.md.

Countries that are not in `countries.json` may take a pattern from `data/regional-defaults.json`. The panel labels those **資料不足／區域推斷** (data-poor / regional inference) and the confidence is low. East Asia has no regional default, so a place such as North Korea stays grey instead of inheriting mainland China’s stack.

YouTube is treated as the video layer. When a country also lists another social platform, the social colour follows that local feed. YouTube stays in the country panel.

## Share a view

Query parameters restore the map:

`?layer=payments&iso=JP&region=east-asia&lang=zh-Hant`

`layer` is `overview`, `social`, `messaging`, `payments`, `search`, or `ai`. `iso` is ISO 3166-1 alpha-2. `region` is an id from `data/regions.json`. `lang` is `zh-Hant` or `en`.

## Keyboard

`/` focuses search. Esc closes the methodology note, the place index, search results, and then the country panel.

The place index (地名索引) is the text alternative to the map.
