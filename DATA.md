# DATA — Internet Nations

Compiled 2026-11-22 (Asia/Shanghai). This file is the methodology. Canonical machine-readable records are in `data/`.

## What this dataset is

A **qualitative, cited atlas** of dominant and secondary platforms in five parts of everyday online life, by country or territory. It is not a market-share spreadsheet. Precise percentages are omitted on purpose: public figures disagree, panels are skewed, and inventing a number would be worse than a ranked list with a year and a link.

## Coverage

- **Full profiles** in `data/countries.json`: about 90 countries and territories with country-specific sources or well-documented regional patterns (confidence `high` or `medium`).
- **Regional inference** in `data/regional-defaults.json`: used only to paint the rest of the map. The UI must show `low` confidence and a “data-poor / regional inference” note.
- Regions follow a practical UN geoscheme-like split (East Asia, Southeast Asia, Western Europe, etc.) so the camera can zoom to a meaningful “neighbourhood”, not only a continent.

Hong Kong, Macao, and Taiwan are separate map entities because their stacks differ from mainland China’s.

## How a “dominant” platform was chosen

For each category, **dominant** means the default or clearly leading platform(s) in everyday use, not the company with the most global MAU. **Secondary** means widely used complements or runners-up.

Rules:

1. Prefer a recent, dated, named source (2025 or 2026) over folklore.
2. Prefer official or primary compilers: DataReportal / Kepios / We Are Social / Meltwater, Similarweb (with the Android caveat), StatCounter (with the referral caveat), central banks and official rails, GSMA, company filings, OpenAI’s own availability list, QuestMobile for China AI (via contemporaneous reporting).
3. When two reputable sources disagree, do not pick a silent winner. Record both in `notes` and lower `confidence` if the lead is the dispute (South Korea search; US / Canada / Australia messaging).
4. Android-only or referral-only panels under-count iMessage, in-app search (Naver), and in-app AI. Notes must say so.
5. Wikipedia was used only as a pointer, never as a sole source for a dominant platform.

## Category notes

### Social

YouTube is often the most-used “social” app worldwide (DataReportal / data.ai, Digital 2025) but is a video layer almost everywhere. The social colour should reflect the distinctive local feed: WeChat / Douyin / Xiaohongshu / Weibo in China; VK in Russia; LINE + X/Instagram in Japan; Facebook or Instagram or TikTok elsewhere as the evidence supports. WhatsApp is classified under Messaging even when GWI lists it as a “favourite social platform”.

### Messaging

Primary 2025 source: [Similarweb, 24 Mar 2025](https://www.similarweb.com/blog/research/apps/worldwide-messaging-apps/) (Android). WhatsApp leads in 70 of 100 countries studied; LINE leads Japan, Taiwan, Thailand; Zalo leads Vietnam; Telegram leads several post-Soviet markets. Similarweb states Messenger did not take the #1 *country* crown in that study, but in the US, Canada, and Australia, Messenger still leads some engagement or install metrics, and **iMessage is missing** from Android panels. Those three plus Ireland are coded `anglosphere-mixed` / messaging mixed, not “WhatsApp only”.

Older compilations (e.g. Ooma, Jan 2025, 143 countries) often named Messenger as #1 in more countries. Where they conflict with Similarweb 2025, Similarweb is preferred and the conflict is noted only when it changes the colour of a large market.

### Payments

Everyday **life-circle** payments: the rail or wallet people actually use for P2P, shops, or transit — Alipay / WeChat Pay, Pix, UPI, M-Pesa, Swish, Vipps MobilePay, PromptPay, PayNow, GCash, MoMo, PayPay, Octopus, Suica/IC, BLIK, iDEAL, Bizum, etc. In card-heavy markets (US, much of Western Europe, Japan for value), say so: cards or Apple Pay / Google Pay may sit alongside a local wallet. Japan: PayPay is the leading QR wallet; Suica/Pasmo/IC remain ubiquitous for transit; cards still take a large share of cashless *value*. Hong Kong: Octopus is near-universal for transit and many shops; FPS, AlipayHK, and cards matter too.

### Search

Google leads almost everywhere. The interesting exceptions are the ones to colour distinctly: **Baidu** (China — StatCounter’s China panel is skewed and should be labelled as such, but all methods still put Baidu first), **Yandex** (Russia), **Naver vs Google** (South Korea — contested: StatCounter referrals often put Google slightly ahead; InternetTrend / local panels often put Naver well ahead because Naver is a walled garden). **Seznam** is a real secondary in Czechia, not a leader. **Yahoo Japan** remains a secondary habit in Japan even as StatCounter shows Google first (and Bing share moving with Yahoo’s backend). DuckDuckGo is almost never a national leader.

StatCounter measures **referrals**, not queries. Official `gs.statcounter.com` pages may block some fetchers; figures used here were cross-checked against compilations that cite StatCounter monthly CSVs (2025–2026).

### AI

[Searchable / StatCounter AI-chatbot referrals, updated Aug 2026](https://www.searchable.com/data/ai-chatbot-market-share): ChatGPT was #1 in 192 of 197 countries (May–Jun 2026 average, ~71% mean country share); Gemini is the usual #2 and the main gainer. This under-counts in-app and workplace use.

**Official availability:** OpenAI’s supported-countries list (fetched 2026-11-22 from [OpenAI Help Centre](https://help.openai.com/en/articles/7947663-chatgpt-and-openai-api-supported-countries-and-territories)) does **not** include mainland China, Hong Kong, Macao, or Russia. Do not colour those places as “ChatGPT lands” just because a global dashboard does. For mainland China, use QuestMobile-reported standalone app MAUs: Doubao leads, then Qwen, then DeepSeek (2026 reporting). For Hong Kong, Macao, and Russia, mark AI as limited / data-poor rather than inventing a leader.

## Primary sources (key list)

| id | Source | Date / vintage | URL |
|---|---|---|---|
| datareportal-2025-global | DataReportal Digital 2025 Global Overview (Kepios / We Are Social / Meltwater) | early 2025 | https://datareportal.com/reports/digital-2025-global-overview-report |
| datareportal-2025-social | DataReportal: top social platforms in 2025 | 2025 | https://datareportal.com/reports/digital-2025-sub-section-top-social-platforms |
| datareportal-2025-china | Digital 2025: China | 2025 | https://datareportal.com/reports/digital-2025-china |
| datareportal-2025-hongkong | Digital 2025: Hong Kong | 2025 | https://datareportal.com/reports/digital-2025-hong-kong |
| datareportal-2025-japan | Digital 2025: Japan | 2025 | https://datareportal.com/reports/digital-2025-japan |
| datareportal-2025-korea | Digital 2025: South Korea (KakaoTalk MAU) | 2025 | https://datareportal.com/reports/digital-2025-south-korea |
| datareportal-2025-thailand | Digital 2025: Thailand (LINE MAU) | 2025 | https://datareportal.com/reports/digital-2025-thailand |
| datareportal-2025-brazil | Digital 2025: Brazil | 2025 | https://datareportal.com/reports/digital-2025-brazil |
| similarweb-messaging-2025 | Similarweb: most popular messaging apps, 100 countries, Android | 24 Mar 2025 | https://www.similarweb.com/blog/research/apps/worldwide-messaging-apps/ |
| statcounter-search-2025-26 | StatCounter Global Stats, search engine referrals, country tables | 2025–2026 monthly | https://gs.statcounter.com/search-engine-market-share |
| searchable-ai-2026 | Searchable: AI chatbot referral share by country (StatCounter) | updated 5 Aug 2026 (May–Jun 2026 average) | https://www.searchable.com/data/ai-chatbot-market-share |
| openai-availability-2026 | OpenAI: ChatGPT and API supported countries | checked 2026-11-22 | https://help.openai.com/en/articles/7947663-chatgpt-and-openai-api-supported-countries-and-territories |
| questmobile-china-ai-2026 | QuestMobile China standalone AI app MAUs, as reported | mid-2026 (June figures widely reported in Aug 2026) | https://technode.com/ and contemporaneous HK01 / 36Kr / Popular in China roundups |
| worldpay-gpr-2026 | Worldpay Global Payments Report 2026 (2025 data), as cited | 2026 | https://www.fintechgenesis.com/post/how-the-world-pays-payment-methods-by-country-and-region |
| gsma-sotir-2026 | GSMA State of the Industry Report on Mobile Money 2026 (Pix 2024 figures) | 2026 | https://www.gsma.com/sotir/ |
| digitalinasia-payments-2026 | Asia Digital Payments Tracker 2026 | 2026 | https://digitalinasia.com/asia-digital-payments-tracker/ |
| korea-times-naver-2026 | Korea Times reporting InternetTrend search shares | 16 Apr 2026 (Mar 2026 average) | https://www.koreatimes.co.kr/ (InternetTrend figures as cited in secondary compilations) |

Additional country digital reports follow the DataReportal pattern `https://datareportal.com/reports/digital-2025-<slug>` and are listed on each country row in `sources.json` / the country record.

## What a v2 should add

- Subnational stacks (mainland China provinces are not uniform; US iMessage vs WhatsApp is coastal/immigrant-skewed).
- A dated time slider (2020 vs 2026).
- Official microdata extracts (NPCI UPI, BCB Pix, Bank of Thailand PromptPay) rather than secondary citations.
- A more careful AI layer (on-device assistants, Naver Cue:, workplace Copilot) once comparable public data exists.
- App stores, short video, and e-commerce as optional layers (App Store / Play, Bilibili / iQiyi, Shopee / Lazada / Amazon).

## Honesty in the UI

If a cell is thin, the map and the panel must say so. A grey country with a clear “資料不足” is a feature, not a hole.
