import { fillFor, patternKey } from "./fill";
import { cameraOf, SUBREGION_TO_REGION, type GeomBits } from "./geo";
import { CONTINENTS, profileFromInference, REGIONS } from "./model";
import { LAYERS, type Profile } from "./types";

export interface GeoFeature {
  type: "Feature";
  id?: string | number;
  properties: Record<string, string>;
  geometry: { type: string; coordinates: unknown };
}

export interface GeoCollection {
  type: "FeatureCollection";
  features: GeoFeature[];
}

export interface JoinResult {
  geoms: Map<string, GeomBits>;
  patterns: string[];
}

export function continentForRegion(region: string, fallback: string): string {
  return REGIONS[region]?.continent || fallback;
}

/** Paint properties and inferred profiles for countries missing from countries.json. */
export function joinCountries(collection: GeoCollection, profiles: Map<string, Profile>): JoinResult {
  const geoms = new Map<string, GeomBits>();
  const patterns = new Set<string>();

  for (const feature of collection.features) {
    const props = feature.properties ?? {};
    feature.properties = props;
    const iso = props.iso || "";
    const region = SUBREGION_TO_REGION[props.subregion] ?? "";
    const continent = continentForRegion(region, props.continent || "");
    let profile = iso ? profiles.get(iso) : undefined;
    const fid = profile?.fid || iso || props.fid || props.name;
    if (!profile) {
      profile = profileFromInference({
        fid,
        iso,
        iso3: props.iso3 || "",
        name: props.name || fid,
        continent: continent || props.continent || "",
        region,
      });
      profiles.set(fid, profile);
    }
    feature.id = fid;
    props.fid = fid;
    const bits = cameraOf(feature.geometry);
    geoms.set(fid, bits);
    for (const layer of LAYERS) {
      const fill = fillFor(profile, layer);
      props[`m_${layer}`] = fill.mode;
      props[`k_${layer}`] = fill.key;
      props[`c_${layer}`] = fill.colors[0];
      props[`u_${layer}`] = profile.inferred ? "1" : "0";
      const pattern = patternKey(fill, profile.inferred);
      props[`p_${layer}`] = pattern;
      if (pattern) patterns.add(pattern);
    }
  }

  return { geoms, patterns: [...patterns] };
}

export function scopeLabel(continent: string, lang: "en" | "zh-Hant"): string {
  return CONTINENTS[continent]?.name[lang] ?? continent;
}
