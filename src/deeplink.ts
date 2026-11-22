import regionsJson from "../data/regions.json";
import { LAYERS, type Lang, type LayerId, type ViewQuery } from "./types";

const REGION_IDS = new Set(Object.keys(regionsJson.regions));

export function isLayer(value: string | null): value is LayerId {
  return !!value && (LAYERS as readonly string[]).includes(value);
}

export function isLang(value: string | null): value is Lang {
  return value === "zh-Hant" || value === "en";
}

function paramsOf(search: string): URLSearchParams {
  const raw = search.startsWith("?") ? search.slice(1) : search;
  return new URLSearchParams(raw);
}

export function parseView(search: string): ViewQuery {
  const q = paramsOf(search);
  const layerRaw = q.get("layer");
  const isoRaw = q.get("iso");
  const regionRaw = q.get("region");
  const langRaw = q.get("lang");
  let iso: string | null = null;
  if (isoRaw && /^[A-Za-z]{2}$/.test(isoRaw)) iso = isoRaw.toUpperCase();
  let region: string | null = null;
  if (regionRaw && REGION_IDS.has(regionRaw)) region = regionRaw;
  return {
    layer: isLayer(layerRaw) ? layerRaw : "overview",
    iso,
    region,
    lang: isLang(langRaw) ? langRaw : null,
  };
}

export function serialize(view: {
  layer: LayerId;
  iso: string | null;
  region: string | null;
  lang: Lang;
}): string {
  const q = new URLSearchParams();
  q.set("layer", view.layer);
  if (view.iso) q.set("iso", view.iso);
  if (view.region) q.set("region", view.region);
  q.set("lang", view.lang);
  return `?${q.toString()}`;
}

/** URL language wins, then a stored preference, then Traditional Chinese. */
export function resolveLang(search: string, stored: string | null): Lang {
  const fromUrl = paramsOf(search).get("lang");
  if (isLang(fromUrl)) return fromUrl;
  if (isLang(stored)) return stored;
  return "zh-Hant";
}
