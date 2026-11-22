# ── Europe helpers ─────────────────────────────────────────────────────────
def eur(iso, iso3, en, zh, region, messaging, payments_dom, payments_sec, pay_notes_en, pay_notes_zh,
        stack="whatsapp-meta", social_dom=None, social_sec=None, search=None, confidence="high", extra_notes=None):
    return C(
        iso=iso, iso3=iso3, name=N(en, zh),
        continent="Europe", region=region, stack=stack,
        year=2025, confidence=confidence,
        social=cat(social_dom or ["instagram", "facebook", "youtube"], social_sec or ["tiktok", "x"],
                   ["datareportal-country-index", "datareportal-2025-social"],
                   "Instagram, Facebook and YouTube are the main public feeds in Western and most European markets; TikTok is a strong secondary, especially among younger users. Facebook skews older in Northern/Western Europe.",
                   "在西歐及多數歐洲市場，Instagram、Facebook、YouTube 是主要公開動態；TikTok 是強次選，尤其在年輕用戶。北歐／西歐的 Facebook 偏年長。", 2025),
        messaging=cat(messaging[0], messaging[1], ["similarweb-messaging-2025"],
                      messaging[2], messaging[3], 2025),
        payments=cat(payments_dom, payments_sec, ["worldpay-gpr-2026"], pay_notes_en, pay_notes_zh, 2025),
        search=search or SEARCH_GOOGLE,
        ai=AI_DEFAULT,
        notes=extra_notes or N("European WhatsApp–Meta or mixed-messaging stack with a local payment rail where one is famous.",
                               "歐洲的 WhatsApp／Meta 或混合通訊組合，若有著名本地支付軌道則一併標出。"),
    )

WA = (["whatsapp"], ["messenger", "telegram", "imessage"],
      "WhatsApp is the default messenger in Similarweb 2025 and regional accounts.",
      "Similarweb 2025 與區域描述都以 WhatsApp 為預設通訊軟體。")

countries.append(eur("DE","DEU","Germany","德國","western-europe", WA,
                     ["girocard", "paypal"], ["cards", "applepay"],
                     "girocard is the domestic debit scheme in store; PayPal is very strong online; invoice / BNPL is a German habit. WhatsApp is chat, not payments.",
                     "店內以 girocard 為本地扣帳體系；網上 PayPal 很強；發票／先買後付是德國習慣。WhatsApp 是聊天，不是支付。",
                     extra_notes=N("WhatsApp-first Europe with a distinctive German payments mix (girocard, PayPal, invoice).",
                                   "以 WhatsApp 為先的歐洲，支付卻很德國（girocard、PayPal、發票）。")))
countries.append(eur("FR","FRA","France","法國","western-europe", WA,
                     ["cartes-bancaires", "cards"], ["paypal", "applepay"],
                     "Cartes Bancaires / co-badged cards are the domestic habit; PayPal and mobile wallets are common online.",
                     "Cartes Bancaires／雙標卡是本地習慣；網上常見 PayPal 與手機錢包。"))
countries.append(eur("NL","NLD","Netherlands","荷蘭","western-europe",
                     (["whatsapp"], ["signal", "imessage"],
                      "WhatsApp is widely used. Similarweb 2025 also flags Signal as number one in the Netherlands on its Android ranking — treat messaging as mixed and note the disagreement rather than silently dropping WhatsApp.",
                      "WhatsApp 使用廣泛。Similarweb 2025 的 Android 排名亦將荷蘭的 Signal 列為首位——通訊應視為混合，並註明分歧，而不是默默拿掉 WhatsApp。"),
                     ["ideal"], ["cards", "wero", "applepay"],
                     "iDEAL has long dominated online bank transfers and is being folded into the European Wero effort. Cards and wallets remain in use.",
                     "iDEAL 長期主導網上銀行轉帳，正被納入歐洲 Wero。卡與錢包仍在使用。",
                     confidence="medium",
                     extra_notes=N("Famous for iDEAL; messaging lead is less clean than in Spain or Germany.",
                                   "以 iDEAL 著名；通訊領先者不像西班牙或德國那般清楚。")))
countries.append(eur("BE","BEL","Belgium","比利時","western-europe", WA,
                     ["bancontact", "cards"], ["applepay", "paypal"],
                     "Bancontact is the distinctive domestic debit scheme; cards and wallets wrap around it.",
                     "Bancontact 是具特色的本地扣帳體系；卡與錢包包在周圍。"))
countries.append(eur("AT","AUT","Austria","奧地利","western-europe", WA,
                     ["cards"], ["applepay", "paypal"],
                     "Card- and wallet-centric, close to the German sphere, without a separately assigned famous rail.",
                     "偏卡與錢包，接近德語圈，不另指定著名軌道。"))
countries.append(eur("CH","CHE","Switzerland","瑞士","western-europe", WA,
                     ["cards", "applepay"], ["paypal"],
                     "Cards and Apple Pay are everyday. TWINT is a well-known local wallet but is not given a monopoly colour here for lack of a primary share table in this compile.",
                     "卡與 Apple Pay 是日常工具。TWINT 是著名本地錢包，但本次彙編缺少第一手市佔表，故不給予壟斷色。",
                     confidence="medium"))
countries.append(eur("LU","LUX","Luxembourg","盧森堡","western-europe", WA,
                     ["cards"], ["paypal", "applepay"],
                     "Small card-centric market.", "細小、偏卡的市場。", confidence="medium"))

countries.append(C(
    iso="GB", iso3="GBR", name=N("United Kingdom", "英國"),
    continent="Europe", region="western-europe", stack="whatsapp-meta",
    year=2025, confidence="high",
    social=cat(["instagram", "youtube", "facebook"], ["tiktok", "x"],
               ["datareportal-country-index", "datareportal-2025-social"],
               "Instagram, YouTube and Facebook are the main public feeds; TikTok is strong among younger users.",
               "Instagram、YouTube、Facebook 是主要公開動態；年輕用戶中 TikTok 很強。", 2025),
    messaging=cat(["whatsapp"], ["imessage", "messenger"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the clear default in Similarweb 2025 (very high Android install penetration). iMessage is common on iPhones.",
                  "Similarweb 2025 顯示 WhatsApp 是清楚的預設（Android 安裝率很高）。iPhone 上 iMessage 很常見。", 2025),
    payments=cat(["cards", "applepay"], ["googlepay", "paypal"],
                 ["worldpay-gpr-2026"],
                 "A card nation going mobile: debit cards still dominate by volume in industry accounts; Apple Pay and Google Pay ride on those cards. Contactless is the habit, not a Pix-like new rail.",
                 "卡之國走向手機：行業描述中扣帳卡筆數仍然最多；Apple Pay 與 Google Pay 建在這些卡上。習慣是感應支付，而不是像 Pix 那樣的新軌道。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("WhatsApp + Meta social + cards/Apple Pay + Google — a northern-European open-web stack.",
            "WhatsApp＋Meta 社交＋卡／Apple Pay＋Google——北歐式開放網絡組合。"),
))

countries.append(C(
    iso="IE", iso3="IRL", name=N("Ireland", "愛爾蘭"),
    continent="Europe", region="western-europe", stack="anglosphere-mixed",
    year=2025, confidence="medium",
    social=cat(["instagram", "facebook", "youtube"], ["tiktok"],
               ["datareportal-country-index"],
               "Close to the UK’s public social mix.",
               "公開社交組合接近英國。", 2025),
    messaging=cat(["whatsapp", "imessage"], ["messenger"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is widely used; iMessage is common. Coded as a light Anglosphere mix rather than a pure WhatsApp country.",
                  "WhatsApp 使用廣泛；iMessage 也很常見。編碼為輕度英語圈混合，而非純粹的 WhatsApp 國家。", 2025),
    payments=cat(["cards", "applepay"], ["paypal"],
                 ["worldpay-gpr-2026"],
                 "Cards and Apple Pay, similar to the UK.",
                 "卡與 Apple Pay，與英國相近。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("Anglosphere-adjacent: WhatsApp plus a strong iMessage / cards layer.",
            "靠近英語圈：WhatsApp，再加上濃厚的 iMessage／卡支付層。"),
))
