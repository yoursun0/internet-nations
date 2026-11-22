export type BBox = [number, number, number, number];
export type Ring = number[][];

export interface GeomBits {
  bbox: BBox;
  label: [number, number];
}

interface Geom {
  type: string;
  coordinates: unknown;
}

export const SUBREGION_TO_REGION: Record<string, string> = {
  "Eastern Asia": "east-asia",
  "South-Eastern Asia": "southeast-asia",
  "Southern Asia": "south-asia",
  "Central Asia": "central-asia",
  "Western Asia": "western-asia",
  "Western Europe": "western-europe",
  "Northern Europe": "northern-europe",
  "Southern Europe": "southern-europe",
  "Eastern Europe": "eastern-europe",
  "Northern America": "northern-america",
  "Central America": "central-america",
  Caribbean: "caribbean",
  "South America": "south-america",
  "Northern Africa": "northern-africa",
  "Western Africa": "western-africa",
  "Eastern Africa": "eastern-africa",
  "Middle Africa": "middle-africa",
  "Southern Africa": "southern-africa",
  "Australia and New Zealand": "australia-nz",
  Melanesia: "pacific",
  Micronesia: "pacific",
  Polynesia: "pacific",
};

function ringsOf(geom: Geom): Ring[] {
  if (geom.type === "Polygon") {
    const polys = geom.coordinates as Ring[];
    return polys[0] ? [polys[0]] : [];
  }
  if (geom.type === "MultiPolygon") {
    const polys = geom.coordinates as Ring[][];
    return polys.map((poly) => poly[0]).filter((ring) => ring && ring.length >= 3);
  }
  return [];
}

function ringArea(ring: Ring): number {
  let area = 0;
  for (let i = 0; i < ring.length - 1; i++) {
    area += ring[i][0] * ring[i + 1][1] - ring[i + 1][0] * ring[i][1];
  }
  return Math.abs(area) / 2;
}

function ringBBox(ring: Ring): BBox {
  let west = Infinity;
  let south = Infinity;
  let east = -Infinity;
  let north = -Infinity;
  for (const [lon, lat] of ring) {
    west = Math.min(west, lon);
    east = Math.max(east, lon);
    south = Math.min(south, lat);
    north = Math.max(north, lat);
  }
  return [west, south, east, north];
}

function vertexAverage(ring: Ring): [number, number] {
  const n = Math.max(1, ring.length - 1);
  let x = 0;
  let y = 0;
  for (let i = 0; i < n; i++) {
    x += ring[i][0];
    y += ring[i][1];
  }
  return [x / n, y / n];
}

/** Camera frame from the largest ring, plus nearby islands that do not make the frame huge. */
export function cameraOf(geom: Geom): GeomBits {
  const rings = ringsOf(geom).map((ring) => ({
    ring,
    area: ringArea(ring),
    bbox: ringBBox(ring),
  }));
  if (!rings.length) return { bbox: [0, 0, 0, 0], label: [0, 0] };
  rings.sort((a, b) => b.area - a.area);
  const main = rings[0];
  let [west, south, east, north] = main.bbox;
  const near = (bbox: BBox) => {
    const cx = (bbox[0] + bbox[2]) / 2;
    const cy = (bbox[1] + bbox[3]) / 2;
    return cx >= west - 25 && cx <= east + 25 && cy >= south - 18 && cy <= north + 18;
  };
  for (const ring of rings.slice(1, 16)) {
    if (!near(ring.bbox)) continue;
    const next: BBox = [
      Math.min(west, ring.bbox[0]),
      Math.min(south, ring.bbox[1]),
      Math.max(east, ring.bbox[2]),
      Math.max(north, ring.bbox[3]),
    ];
    if (next[2] - next[0] > 80) continue;
    [west, south, east, north] = next;
  }
  return { bbox: [west, south, east, north], label: vertexAverage(main.ring) };
}

export function graticule(): {
  type: "FeatureCollection";
  features: {
    type: "Feature";
    properties: Record<string, never>;
    geometry: { type: "LineString"; coordinates: number[][] };
  }[];
} {
  const features: {
    type: "Feature";
    properties: Record<string, never>;
    geometry: { type: "LineString"; coordinates: number[][] };
  }[] = [];
  for (let lon = -180; lon <= 180; lon += 30) {
    features.push({
      type: "Feature",
      properties: {},
      geometry: {
        type: "LineString",
        coordinates: [
          [lon, -62],
          [lon, 78],
        ],
      },
    });
  }
  for (let lat = -60; lat <= 60; lat += 30) {
    features.push({
      type: "Feature",
      properties: {},
      geometry: {
        type: "LineString",
        coordinates: [
          [-180, lat],
          [180, lat],
        ],
      },
    });
  }
  return { type: "FeatureCollection", features };
}
