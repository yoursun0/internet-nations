import { expect, test } from "bun:test";
import { I18N, t } from "../src/i18n";

test("zh-Hant and en expose the same non-empty keys", () => {
  const zh = Object.keys(I18N["zh-Hant"]).sort();
  const en = Object.keys(I18N.en).sort();
  expect(zh).toEqual(en);
  for (const key of zh) {
    expect(I18N["zh-Hant"][key].length).toBeGreaterThan(0);
    expect(I18N.en[key].length).toBeGreaterThan(0);
  }
});

test("required chrome and the data-poor label exist in both languages", () => {
  for (const key of [
    "layer.overview",
    "layer.social",
    "layer.messaging",
    "layer.payments",
    "layer.search",
    "layer.ai",
    "legend.inferred",
    "panel.inferred",
    "stack.wechat-superapp",
    "stack.unknown",
    "about.p3",
    "about.p6",
    "about.open",
    "about.sources",
    "chrome.hide",
    "chrome.show",
  ]) {
    expect(t("zh-Hant", key).length).toBeGreaterThan(0);
    expect(t("en", key).length).toBeGreaterThan(0);
  }
  expect(t("zh-Hant", "panel.inferred")).toBe("資料不足／區域推斷");
  expect(t("zh-Hant", "legend.inferred")).toBe("資料不足／區域推斷");
  expect(t("en", "panel.inferred").toLowerCase()).toContain("data-poor");
  expect(t("zh-Hant", "chrome.hide")).toBe("隱藏選單");
  expect(t("en", "chrome.hide")).toBe("Hide menu");
  expect(t("zh-Hant", "chrome.show")).toBe("顯示選單");
  expect(t("en", "chrome.show")).toBe("Show menu");
  expect(t("zh-Hant", "about.open")).toBe("方法");
  expect(t("en", "about.open")).toBe("Method");
});
