import { platformColor } from "./model";
import { NODATA, STACK_COLOR, type LayerId, type Profile } from "./types";

export interface Fill {
  mode: "solid" | "split" | "nodata";
  key: string;
  ids: string[];
  colors: string[];
}

/** Messaging markets the notes refuse to award to one app. */
const MESSAGING_MIX = new Set(["US", "CA", "AU", "IE", "NZ"]);

/**
 * Split fills are only for leads the sources refuse to rank:
 * Korea search, Alipay + WeChat Pay, and the Anglosphere messaging mix,
 * plus notes that explicitly say contested, duopoly, or a pair.
 * A longer dominant list is not itself a split — social stays one colour.
 */
export function isContested(profile: Profile, layer: LayerId): boolean {
  if (layer === "overview") return false;
  const cell = profile[layer];
  const dom = cell.dominant;
  const en = cell.notes.en ?? "";
  if (layer === "search" && profile.iso === "KR" && dom.length >= 2) return true;
  if (layer === "payments" && dom.includes("alipay") && dom.includes("wechatpay")) return true;
  if (layer === "messaging" && MESSAGING_MIX.has(profile.iso) && dom.length >= 2) return true;
  if (dom.length < 2) return false;
  if (/contested|duopoly|treat as a pair|local pair/i.test(en)) return true;
  if (layer === "messaging" && /\bmixed\b/i.test(en)) return true;
  return false;
}

export function fillFor(profile: Profile, layer: LayerId): Fill {
  if (layer === "overview") {
    if (!profile.stack || profile.stack === "unknown") {
      return { mode: "nodata", key: "nodata", ids: [], colors: [NODATA] };
    }
    const color = STACK_COLOR[profile.stack] ?? NODATA;
    return { mode: "solid", key: profile.stack, ids: [profile.stack], colors: [color] };
  }

  const dom = profile[layer].dominant;
  if (isContested(profile, layer)) {
    const ids = dom.slice(0, 3);
    return {
      mode: "split",
      key: ids.join("+"),
      ids,
      colors: ids.map((id) => platformColor(id)),
    };
  }

  let id = dom[0];
  // YouTube is the video layer almost everywhere. Colour the local feed instead.
  if (layer === "social") {
    const rest = dom.filter((item) => item !== "youtube");
    if (rest.length) id = rest[0];
  }
  if (!id) return { mode: "nodata", key: "nodata", ids: [], colors: [NODATA] };
  return { mode: "solid", key: id, ids: [id], colors: [platformColor(id)] };
}

export function patternKey(fill: Fill, inferred: boolean): string {
  if (fill.mode === "split") return `split:${fill.ids.join("+")}`;
  if (inferred) return `wash:${(fill.colors[0] ?? NODATA).replace("#", "")}`;
  return "";
}
