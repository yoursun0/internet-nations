import countriesJson from "../data/countries.json";
import defaultsJson from "../data/regional-defaults.json";
import platformsJson from "../data/platforms.json";
import regionsJson from "../data/regions.json";
import sourcesJson from "../data/sources.json";
import type { Bilingual, CatId, Cell, Confidence, Profile } from "./types";
import { CATS } from "./types";

export interface PlatformRec {
  name: Bilingual;
  category: string[];
  color: string;
}

export interface SourceRec {
  title: string;
  publisher: string;
  year: number;
  url: string;
}

export interface RegionRec {
  name: Bilingual;
  continent?: string;
  bbox: [number, number, number, number];
}

interface DefaultRec {
  stack: string;
  social: string[];
  messaging: string[];
  payments: string[];
  search: string[];
  ai: string[];
  notes: Bilingual;
  confidence: string;
  year: number;
}

export const PLATFORMS = platformsJson.platforms as Record<string, PlatformRec>;
export const SOURCES = sourcesJson.sources as Record<string, SourceRec>;
export const REGIONS = regionsJson.regions as unknown as Record<string, RegionRec>;
export const CONTINENTS = regionsJson.continents as unknown as Record<string, RegionRec>;
const DEFAULTS = defaultsJson.defaults as Record<string, DefaultRec>;

export const LAYER_SOURCE_IDS: Record<string, string[]> = {
  overview: ["datareportal-2025-global", "datareportal-2025-social"],
  social: ["datareportal-2025-social", "datareportal-2025-global"],
  messaging: ["similarweb-messaging-2025"],
  payments: ["worldpay-gpr-2026", "digitalinasia-payments-2026", "gsma-sotir-2026"],
  search: ["statcounter-search", "korea-search-conflict-2026"],
  ai: ["searchable-ai-2026", "openai-availability-2026", "questmobile-china-ai-2026"],
};

function asCell(cell: Cell): Cell {
  return {
    dominant: cell.dominant ?? [],
    secondary: cell.secondary ?? [],
    notes: cell.notes,
    sources: cell.sources ?? [],
    year: cell.year,
  };
}

export function profileFromCountry(row: (typeof countriesJson.countries)[number]): Profile {
  return {
    fid: row.iso,
    iso: row.iso,
    iso3: row.iso3,
    name: row.name,
    continent: row.continent,
    region: row.region,
    stack: row.stack,
    year: row.year,
    confidence: row.confidence as Confidence,
    social: asCell(row.social),
    messaging: asCell(row.messaging),
    payments: asCell(row.payments),
    search: asCell(row.search),
    ai: asCell(row.ai),
    notes: row.notes,
    inferred: false,
  };
}

const NO_DEFAULT_NOTES: Bilingual = {
  en: "No full profile and no regional pattern. Shown as data-poor, not as a neighbour’s stack.",
  "zh-Hant": "沒有完整檔案，也沒有區域推斷可用。以資料不足顯示，不會套用鄰國的生活圈。",
};

function blankCell(notes: Bilingual, dominant: string[] = []): Cell {
  return { dominant, secondary: [], notes, sources: [] };
}

export function profileFromInference(opts: {
  fid: string;
  iso: string;
  iso3: string;
  name: string;
  continent: string;
  region: string;
}): Profile {
  const def = opts.region ? DEFAULTS[opts.region] : undefined;
  const name = { en: opts.name, "zh-Hant": opts.name };
  if (!def) {
    return {
      fid: opts.fid,
      iso: opts.iso,
      iso3: opts.iso3,
      name,
      continent: opts.continent,
      region: opts.region,
      stack: "unknown",
      year: 2025,
      confidence: "low",
      social: blankCell(NO_DEFAULT_NOTES),
      messaging: blankCell(NO_DEFAULT_NOTES),
      payments: blankCell(NO_DEFAULT_NOTES),
      search: blankCell(NO_DEFAULT_NOTES),
      ai: blankCell(NO_DEFAULT_NOTES),
      notes: NO_DEFAULT_NOTES,
      inferred: true,
    };
  }
  const notes = def.notes;
  return {
    fid: opts.fid,
    iso: opts.iso,
    iso3: opts.iso3,
    name,
    continent: opts.continent || defContinent(opts.region),
    region: opts.region,
    stack: def.stack,
    year: def.year,
    confidence: "low",
    social: blankCell(notes, def.social),
    messaging: blankCell(notes, def.messaging),
    payments: blankCell(notes, def.payments),
    search: blankCell(notes, def.search),
    ai: blankCell(notes, def.ai),
    notes,
    inferred: true,
  };
}

function defContinent(region: string): string {
  return REGIONS[region]?.continent ?? "";
}

let cached: Map<string, Profile> | null = null;

export function profilesFromDataset(): Map<string, Profile> {
  if (!cached) {
    cached = new Map(countriesJson.countries.map((row) => [row.iso, profileFromCountry(row)]));
  }
  return cached;
}

export function profileByIso(iso: string): Profile | undefined {
  return profilesFromDataset().get(iso);
}

export function platformName(id: string, lang: "en" | "zh-Hant"): string {
  return PLATFORMS[id]?.name[lang] ?? id;
}

export function platformColor(id: string): string {
  return PLATFORMS[id]?.color ?? "#888888";
}

export function sourceList(profile: Profile): string[] {
  const out: string[] = [];
  const seen = new Set<string>();
  for (const cat of CATS) {
    for (const id of profile[cat].sources) {
      if (!seen.has(id)) {
        seen.add(id);
        out.push(id);
      }
    }
  }
  return out;
}

export function cellOf(profile: Profile, cat: CatId): Cell {
  return profile[cat];
}
