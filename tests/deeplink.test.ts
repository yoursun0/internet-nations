import { expect, test } from "bun:test";
import { parseView, resolveLang, serialize } from "../src/deeplink";

test("round-trips layer, iso, region, and lang", () => {
  const query = "?layer=payments&iso=JP&region=east-asia&lang=zh-Hant";
  const parsed = parseView(query);
  expect(parsed).toEqual({
    layer: "payments",
    iso: "JP",
    region: "east-asia",
    lang: "zh-Hant",
  });
  expect(serialize({ ...parsed, lang: "zh-Hant" })).toBe(query);
});

test("normalises iso and drops unknown layer, region, and lang", () => {
  expect(parseView("?layer=nope&iso=jp&region=atlantis&lang=fr")).toEqual({
    layer: "overview",
    iso: "JP",
    region: null,
    lang: null,
  });
  expect(parseView("").layer).toBe("overview");
  expect(serialize({ layer: "ai", iso: null, region: "western-europe", lang: "en" })).toBe(
    "?layer=ai&region=western-europe&lang=en",
  );
});

test("language falls back from the URL to storage to Traditional Chinese", () => {
  expect(resolveLang("?lang=en", "zh-Hant")).toBe("en");
  expect(resolveLang("?layer=social", "en")).toBe("en");
  expect(resolveLang("", null)).toBe("zh-Hant");
  expect(resolveLang("?lang=fr", "nope")).toBe("zh-Hant");
});
