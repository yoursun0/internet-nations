import { expect, test } from "bun:test";
import { fillFor } from "../src/fill";
import { profileByIso, profileFromInference } from "../src/model";

function profile(iso: string) {
  const row = profileByIso(iso);
  if (!row) throw new Error(iso);
  return row;
}

test("does not invent a single winner for contested leads", () => {
  const korea = fillFor(profile("KR"), "search");
  expect(korea.mode).toBe("split");
  expect(korea.ids).toEqual(["naver", "google"]);

  const chinaPay = fillFor(profile("CN"), "payments");
  expect(chinaPay.mode).toBe("split");
  expect(chinaPay.ids).toContain("alipay");
  expect(chinaPay.ids).toContain("wechatpay");

  for (const iso of ["US", "CA", "AU", "IE", "NZ"]) {
    const messaging = fillFor(profile(iso), "messaging");
    expect(messaging.mode).toBe("split");
    expect(messaging.ids).toContain("imessage");
  }
});

test("does not colour China, Hong Kong, Macao, or Russia as ChatGPT", () => {
  expect(fillFor(profile("CN"), "ai").ids).toEqual(["doubao"]);
  expect(fillFor(profile("CN"), "ai").ids).not.toContain("chatgpt");
  for (const iso of ["HK", "MO", "RU"]) {
    const ai = fillFor(profile(iso), "ai");
    expect(ai.mode).toBe("nodata");
    expect(ai.ids).not.toContain("chatgpt");
  }
  expect(profile("HK").stack).toBe("whatsapp-meta");
  expect(profile("CN").stack).toBe("wechat-superapp");
});

test("social colour skips YouTube when a local feed is also listed", () => {
  expect(fillFor(profile("US"), "social").ids[0]).not.toBe("youtube");
  expect(fillFor(profile("JP"), "social").ids).toEqual(["x"]);
  expect(fillFor(profile("CN"), "social").ids).toEqual(["wechat"]);
  expect(fillFor(profile("JP"), "messaging")).toEqual(
    expect.objectContaining({ mode: "solid", ids: ["line"] }),
  );
});

test("places without a full profile stay low-confidence and data-poor", () => {
  const timor = profileFromInference({
    fid: "XX",
    iso: "XX",
    iso3: "XXX",
    name: "Example",
    continent: "Asia",
    region: "southeast-asia",
  });
  expect(timor.inferred).toBe(true);
  expect(timor.confidence).toBe("low");
  expect(fillFor(timor, "messaging").ids).toEqual(["whatsapp"]);

  const northKorea = profileFromInference({
    fid: "KP",
    iso: "KP",
    iso3: "PRK",
    name: "North Korea",
    continent: "Asia",
    region: "east-asia",
  });
  expect(northKorea.inferred).toBe(true);
  expect(northKorea.stack).toBe("unknown");
  expect(fillFor(northKorea, "overview").mode).toBe("nodata");
  expect(fillFor(northKorea, "ai").ids).not.toContain("chatgpt");
  expect(fillFor(northKorea, "messaging").mode).toBe("nodata");
});
