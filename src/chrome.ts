/** Keep in sync with the inline script in index.html and the 959px media query. */
export const CHROME_HIDE_KEY = "internet-nations-hide-chrome";

/** Matches `@media (max-width: 959px)` in styles.css. */
export const MOBILE_CHROME_MAX_PX = 959;

export interface ChromeStorage {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
  removeItem(key: string): void;
}

export function readHideChrome(storage: Pick<ChromeStorage, "getItem"> | null): boolean {
  try {
    return storage?.getItem(CHROME_HIDE_KEY) === "1";
  } catch {
    return false;
  }
}

export function writeHideChrome(storage: Pick<ChromeStorage, "setItem" | "removeItem"> | null, hidden: boolean): void {
  try {
    if (!storage) return;
    if (hidden) storage.setItem(CHROME_HIDE_KEY, "1");
    else storage.removeItem(CHROME_HIDE_KEY);
  } catch {
    /* private mode or blocked storage */
  }
}

/** Saved preference takes effect only on the mobile layout. Desktop always shows the masthead. */
export function chromeHiddenActive(prefersHidden: boolean, viewportWidth: number): boolean {
  return prefersHidden && viewportWidth <= MOBILE_CHROME_MAX_PX;
}
