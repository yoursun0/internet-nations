import { expect, test } from "bun:test";
import {
  CHROME_HIDE_KEY,
  MOBILE_CHROME_MAX_PX,
  chromeHiddenActive,
  readHideChrome,
  writeHideChrome,
  type ChromeStorage,
} from "../src/chrome";

function memoryStorage(): ChromeStorage & { dump(): Map<string, string> } {
  const mem = new Map<string, string>();
  return {
    getItem: (key) => mem.get(key) ?? null,
    setItem: (key, value) => {
      mem.set(key, value);
    },
    removeItem: (key) => {
      mem.delete(key);
    },
    dump: () => mem,
  };
}

test("hidden chrome applies only at the mobile breakpoint", () => {
  expect(MOBILE_CHROME_MAX_PX).toBe(959);
  expect(chromeHiddenActive(true, 390)).toBe(true);
  expect(chromeHiddenActive(true, 959)).toBe(true);
  expect(chromeHiddenActive(true, 960)).toBe(false);
  expect(chromeHiddenActive(true, 1280)).toBe(false);
  expect(chromeHiddenActive(false, 390)).toBe(false);
  expect(chromeHiddenActive(false, 1280)).toBe(false);
});

test("hide-chrome preference round-trips through storage", () => {
  const storage = memoryStorage();
  expect(readHideChrome(storage)).toBe(false);
  writeHideChrome(storage, true);
  expect(storage.getItem(CHROME_HIDE_KEY)).toBe("1");
  expect(readHideChrome(storage)).toBe(true);
  writeHideChrome(storage, false);
  expect(readHideChrome(storage)).toBe(false);
  expect(storage.dump().has(CHROME_HIDE_KEY)).toBe(false);
});

test("unavailable storage does not throw", () => {
  const broken: ChromeStorage = {
    getItem: () => {
      throw new Error("blocked");
    },
    setItem: () => {
      throw new Error("blocked");
    },
    removeItem: () => {
      throw new Error("blocked");
    },
  };
  expect(readHideChrome(broken)).toBe(false);
  expect(readHideChrome(null)).toBe(false);
  writeHideChrome(broken, true);
  writeHideChrome(null, false);
});
