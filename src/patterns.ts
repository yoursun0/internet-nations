import type maplibregl from "maplibre-gl";
import { platformColor } from "./model";

const ready = new Set<string>();

function stripeImage(colors: string[]): ImageData {
  const stripe = 8;
  const size = Math.max(stripe, stripe * colors.length);
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext("2d");
  if (!ctx) throw new Error("canvas");
  colors.forEach((color, index) => {
    ctx.fillStyle = color;
    ctx.fillRect(index * stripe, 0, stripe, size);
  });
  return ctx.getImageData(0, 0, size, size);
}

function washImage(color: string): ImageData {
  const size = 16;
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext("2d");
  if (!ctx) throw new Error("canvas");
  ctx.fillStyle = color;
  ctx.fillRect(0, 0, size, size);
  ctx.fillStyle = "rgba(243, 238, 228, 0.72)";
  for (let y = 2; y < size; y += 4) {
    for (let x = y % 8 === 2 ? 2 : 0; x < size; x += 8) {
      ctx.fillRect(x, y, 2, 2);
    }
  }
  return ctx.getImageData(0, 0, size, size);
}

export function patternSpec(id: string): { colors: string[]; wash: boolean } | null {
  if (id.startsWith("split:")) {
    const ids = id.slice("split:".length).split("+").filter(Boolean);
    return { colors: ids.map((item) => platformColor(item)), wash: false };
  }
  if (id.startsWith("wash:")) {
    const hex = id.slice("wash:".length);
    return { colors: [hex.startsWith("#") ? hex : `#${hex}`], wash: true };
  }
  return null;
}

export function ensurePattern(map: maplibregl.Map, id: string): void {
  if (!id || ready.has(id) || map.hasImage(id)) {
    if (id) ready.add(id);
    return;
  }
  const spec = patternSpec(id);
  if (!spec || !spec.colors.length) return;
  const image = spec.wash ? washImage(spec.colors[0]) : stripeImage(spec.colors);
  map.addImage(id, image);
  ready.add(id);
}
