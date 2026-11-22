import { expect, test } from "bun:test";
import countriesJson from "../data/countries.json";
import defaultsJson from "../data/regional-defaults.json";
import platformsJson from "../data/platforms.json";
import regionsJson from "../data/regions.json";
import sourcesJson from "../data/sources.json";
import { STACK_IDS } from "../src/types";

const CATS = ["social", "messaging", "payments", "search", "ai"] as const;
const stacks = new Set<string>(STACK_IDS);

test("country profiles are unique and complete", () => {
  const rows = countriesJson.countries;
  expect(rows.length).toBeGreaterThan(100);
  const isos = rows.map((row) => row.iso);
  const iso3s = rows.map((row) => row.iso3);
  expect(new Set(isos).size).toBe(isos.length);
  expect(new Set(iso3s).size).toBe(iso3s.length);

  for (const row of rows) {
    expect(row.iso).toMatch(/^[A-Z]{2}$/);
    expect(row.iso3).toMatch(/^[A-Z]{3}$/);
    expect(row.name.en.length).toBeGreaterThan(0);
    expect(row.name["zh-Hant"].length).toBeGreaterThan(0);
    expect(regionsJson.continents[row.continent as keyof typeof regionsJson.continents]).toBeTruthy();
    expect(regionsJson.regions[row.region as keyof typeof regionsJson.regions]).toBeTruthy();
    expect(stacks.has(row.stack)).toBe(true);
    expect(["high", "medium", "low"]).toContain(row.confidence);
    expect(typeof row.year).toBe("number");
    expect(row.notes.en.length).toBeGreaterThan(0);
    expect(row.notes["zh-Hant"].length).toBeGreaterThan(0);

    for (const cat of CATS) {
      const cell = row[cat];
      expect(Array.isArray(cell.dominant)).toBe(true);
      expect(Array.isArray(cell.secondary)).toBe(true);
      expect(cell.dominant.length).toBeLessThanOrEqual(3);
      for (const id of [...cell.dominant, ...cell.secondary]) {
        expect(platformsJson.platforms[id as keyof typeof platformsJson.platforms]).toBeTruthy();
      }
      for (const sourceId of cell.sources) {
        expect(sourcesJson.sources[sourceId as keyof typeof sourcesJson.sources]).toBeTruthy();
      }
      expect(cell.notes.en.length).toBeGreaterThan(0);
      expect(cell.notes["zh-Hant"].length).toBeGreaterThan(0);
    }
  }
});

test("every continent and region has a bbox", () => {
  for (const group of [regionsJson.continents, regionsJson.regions]) {
    for (const rec of Object.values(group)) {
      expect(rec.bbox).toHaveLength(4);
      for (const n of rec.bbox) expect(typeof n).toBe("number");
      expect(rec.bbox[0]).toBeLessThan(rec.bbox[2]);
      expect(rec.bbox[1]).toBeLessThan(rec.bbox[3]);
      expect(rec.name.en.length).toBeGreaterThan(0);
      expect(rec.name["zh-Hant"].length).toBeGreaterThan(0);
    }
  }
});

test("regional defaults point at real regions and platforms", () => {
  for (const [region, def] of Object.entries(defaultsJson.defaults)) {
    expect(regionsJson.regions[region as keyof typeof regionsJson.regions]).toBeTruthy();
    expect(stacks.has(def.stack)).toBe(true);
    expect(def.confidence).toBe("low");
    for (const cat of CATS) {
      for (const id of def[cat]) {
        expect(platformsJson.platforms[id as keyof typeof platformsJson.platforms]).toBeTruthy();
      }
    }
    expect(def.notes.en.length).toBeGreaterThan(0);
    expect(def.notes["zh-Hant"].length).toBeGreaterThan(0);
  }
});
