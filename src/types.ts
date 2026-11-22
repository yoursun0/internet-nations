export const LAYERS = ["overview", "social", "messaging", "payments", "search", "ai"] as const;
export type LayerId = (typeof LAYERS)[number];

export const CATS = ["social", "messaging", "payments", "search", "ai"] as const;
export type CatId = (typeof CATS)[number];

export type Lang = "zh-Hant" | "en";

export type Confidence = "high" | "medium" | "low";

export interface Bilingual {
  en: string;
  "zh-Hant": string;
}

export interface Cell {
  dominant: string[];
  secondary: string[];
  notes: Bilingual;
  sources: string[];
  year?: number;
}

export interface Profile {
  fid: string;
  iso: string;
  iso3: string;
  name: Bilingual;
  continent: string;
  region: string;
  stack: string;
  year: number;
  confidence: Confidence;
  social: Cell;
  messaging: Cell;
  payments: Cell;
  search: Cell;
  ai: Cell;
  notes: Bilingual;
  /** True when the country is not a full profile in countries.json. */
  inferred: boolean;
}

export interface ViewQuery {
  layer: LayerId;
  iso: string | null;
  region: string | null;
  lang: Lang | null;
}

export const LANG_KEY = "internet-nations.lang";

export const NODATA = "#E4DCCD";

export const STACK_IDS = [
  "wechat-superapp",
  "line-sphere",
  "kakao-naver",
  "zalo-hybrid",
  "vk-yandex",
  "whatsapp-meta",
  "anglosphere-mixed",
  "unknown",
] as const;

export const STACK_COLOR: Record<string, string> = {
  "wechat-superapp": "#2DBE64",
  "line-sphere": "#00B900",
  "kakao-naver": "#FEE500",
  "zalo-hybrid": "#0068FF",
  "vk-yandex": "#0077FF",
  "whatsapp-meta": "#128C7E",
  "anglosphere-mixed": "#6E6256",
  unknown: NODATA,
};

export const CONTINENT_ORDER = [
  "Asia",
  "Europe",
  "Africa",
  "North America",
  "South America",
  "Oceania",
] as const;

export const WORLD_BBOX: [number, number, number, number] = [-168, -56, 190, 78];
