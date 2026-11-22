# ── Americas ───────────────────────────────────────────────────────────────
countries.append(C(
    iso="US", iso3="USA", name=N("United States", "美國"),
    continent="North America", region="northern-america", stack="anglosphere-mixed",
    year=2025, confidence="high",
    social=cat(["youtube", "instagram", "facebook"], ["tiktok", "x", "reddit", "snapchat"],
               ["datareportal-2025-usa", "datareportal-2025-social"],
               "A wide portfolio: YouTube, Instagram and Facebook are the mass public layers; TikTok, X, Reddit and Snapchat are important subcultures. No single national social app in the WeChat or LINE sense.",
               "組合很廣：YouTube、Instagram、Facebook 是大眾公開層；TikTok、X、Reddit、Snapchat 是重要次文化。沒有微信或 LINE 那種單一全國社交 App。", 2025),
    messaging=cat(["imessage", "whatsapp", "messenger"], ["snapchat", "telegram"],
                  ["similarweb-messaging-2025"],
                  "MIXED, and Android panels mislead. Similarweb 2025 ranks WhatsApp first on some Android metrics, but Messenger leads some US engagement / MAU measures, and iMessage is the default on iPhones (a large share of the market) and is invisible to Android studies. Show a mixed fill, not WhatsApp-only.",
                  "混合，而且 Android 面板會誤導。Similarweb 2025 在部分 Android 指標把 WhatsApp 列第一，但 Messenger 在部分美國活躍／月活指標領先；iMessage 是 iPhone（市場很大一部分）的預設，且 Android 研究看不見。應顯示混合，而不是只有 WhatsApp。", 2025),
    payments=cat(["cards", "applepay"], ["venmo", "zelle", "paypal", "googlepay"],
                 ["worldpay-gpr-2026"],
                 "A card-and-rewards culture: credit and debit cards still dominate in-store value in industry accounts. Apple Pay / Google Pay ride on those cards. Venmo, Zelle and PayPal are the distinctive P2P layer — not a Pix or UPI equivalent.",
                 "卡與回贈文化：行業描述中，店內金額仍以信用／扣帳卡為主。Apple Pay／Google Pay 建在這些卡上。Venmo、Zelle、PayPal 是具特色的 P2P 層——不是 Pix 或 UPI 的對等物。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("The Anglosphere mixed stack: many social apps, iMessage/Messenger/WhatsApp together, cards + Apple Pay + Venmo/Zelle, Google, ChatGPT.",
            "英語圈混合組合：社交 App 很多，iMessage／Messenger／WhatsApp 並存，卡＋Apple Pay＋Venmo／Zelle，搜尋 Google，AI 為 ChatGPT。"),
))

countries.append(C(
    iso="CA", iso3="CAN", name=N("Canada", "加拿大"),
    continent="North America", region="northern-america", stack="anglosphere-mixed",
    year=2025, confidence="high",
    social=cat(["youtube", "instagram", "facebook"], ["tiktok", "x"],
               ["datareportal-country-index", "datareportal-2025-social"],
               "Close to the US public social mix.",
               "公開社交組合接近美國。", 2025),
    messaging=cat(["imessage", "whatsapp", "messenger"], [],
                  ["similarweb-messaging-2025"],
                  "MIXED. Similarweb 2025: WhatsApp leads some download / active-use metrics; Messenger leads some install measures. iMessage is common on iPhones and missing from Android panels.",
                  "混合。Similarweb 2025：WhatsApp 在部分下載／活躍指標領先；Messenger 在部分安裝指標領先。iPhone 上 iMessage 很常見，Android 面板看不到。", 2025),
    payments=cat(["cards", "applepay"], ["paypal", "googlepay"],
                 ["worldpay-gpr-2026"],
                 "Cards and Interac / Apple Pay are everyday. No Pix-like rail is assigned.",
                 "卡與 Interac／Apple Pay 是日常工具。不指定類似 Pix 的軌道。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("Anglosphere mixed, close to the United States.", "英語圈混合，接近美國。"),
))

countries.append(C(
    iso="MX", iso3="MEX", name=N("Mexico", "墨西哥"),
    continent="North America", region="central-america", stack="whatsapp-meta",
    year=2025, confidence="high",
    social=cat(["facebook", "instagram", "youtube"], ["tiktok"],
               ["datareportal-country-index", "datareportal-2025-social"],
               "Facebook, Instagram and YouTube are the mass public layers; TikTok is strong.",
               "Facebook、Instagram、YouTube 是大眾公開層；TikTok 很強。", 2025),
    messaging=cat(["whatsapp"], ["messenger"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the default national chat in Similarweb 2025.",
                  "Similarweb 2025 以 WhatsApp 為全國預設聊天工具。", 2025),
    payments=cat(["cards", "mercadopago"], ["paypal"],
                 ["worldpay-gpr-2026"],
                 "Cards, cash-adjacent methods (for example OXXO) and Mercado Pago matter. Not a Pix-universal market.",
                 "卡、接近現金的方式（如 OXXO）與 Mercado Pago 都很重要。不是 Pix 那樣近乎全民的市場。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("Spanish-speaking WhatsApp–Meta, with Mercado Pago and cards rather than a single instant rail.",
            "西班牙語的 WhatsApp／Meta，支付是 Mercado Pago 與卡，而不是單一即時軌道。"),
))

for iso, iso3, en, zh, region, conf in [
    ("GT","GTM","Guatemala","危地馬拉","central-america","medium"),
    ("CR","CRI","Costa Rica","哥斯達黎加","central-america","medium"),
    ("PA","PAN","Panama","巴拿馬","central-america","medium"),
    ("HN","HND","Honduras","洪都拉斯","central-america","medium"),
    ("SV","SLV","El Salvador","薩爾瓦多","central-america","medium"),
    ("NI","NIC","Nicaragua","尼加拉瓜","central-america","low"),
    ("DO","DOM","Dominican Republic","多明尼加","caribbean","medium"),
    ("CU","CUB","Cuba","古巴","caribbean","low"),
    ("JM","JAM","Jamaica","牙買加","caribbean","medium"),
    ("HT","HTI","Haiti","海地","caribbean","low"),
    ("PR","PRI","Puerto Rico","波多黎各","caribbean","medium"),
    ("TT","TTO","Trinidad and Tobago","千里達及托巴哥","caribbean","low"),
]:
    msg_dom = ["whatsapp"]
    msg_note_en = "WhatsApp is the regional default."
    msg_note_zh = "區域預設為 WhatsApp。"
    if iso in {"DO", "PA"}:
        msg_note_en = "Similarweb 2025 flags Snapchat as number one in some Central American / Caribbean markets including Panama and the Dominican Republic. WhatsApp and Messenger remain widely used — treat as mixed, medium confidence."
        msg_note_zh = "Similarweb 2025 將部分中美／加勒比市場（包括巴拿馬與多明尼加）的 Snapchat 列為首位。WhatsApp 與 Messenger 仍然常用——視為混合，信心中等。"
        msg_dom = ["whatsapp", "snapchat"]
    is_cu = iso == "CU"
    countries.append(C(
        iso=iso, iso3=iso3, name=N(en, zh),
        continent="North America", region=region,
        stack="unknown" if is_cu else "whatsapp-meta",
        year=2025, confidence="low" if is_cu else conf,
        social=cat(["facebook", "instagram"], ["youtube", "tiktok"],
                   ["datareportal-country-index"],
                   "Facebook and Instagram are the usual public layer. Cuba is data-poor because of access constraints.",
                   "通常以 Facebook 與 Instagram 為公開層。古巴因訪問限制而資料不足。", 2025),
        messaging=cat(msg_dom, ["messenger"], ["similarweb-messaging-2025"], msg_note_en, msg_note_zh, 2025),
        payments=cat(["cards"], [], ["worldpay-gpr-2026"],
                     "Data-poor; international payment brands are a poor guide." if is_cu
                     else "Cards, cash and regional wallets; no high-confidence national rail.",
                     "資料不足；國際支付品牌不是好的指南。" if is_cu else "卡、現金與區域錢包；不以高信心指定國家軌道。", 2025),
        search=SEARCH_GOOGLE if not is_cu else cat(["google"], [], ["statcounter-search"],
                                                     "Access is constrained; do not over-read a referral panel.",
                                                     "訪問受限；不要過度解讀轉介面板。", 2026),
        ai=AI_DEFAULT if not is_cu else cat([], [], ["openai-availability-2026"],
                                              "Data-poor; no AI leader assigned.",
                                              "資料不足；不指定 AI 領導產品。", 2026),
        notes=N("Data-poor: access constraints make defaults unstable." if is_cu
                else "Central American / Caribbean WhatsApp–Meta pattern, with thinner tables than Mexico or Brazil.",
                "資料不足：訪問限制令預設不穩定。" if is_cu
                else "中美／加勒比的 WhatsApp／Meta 格局，表薄於墨西哥或巴西。"),
    ))

countries.append(C(
    iso="BR", iso3="BRA", name=N("Brazil", "巴西"),
    continent="South America", region="south-america", stack="whatsapp-meta",
    year=2025, confidence="high",
    social=cat(["instagram", "youtube", "facebook"], ["tiktok", "whatsapp"],
               ["datareportal-2025-brazil", "datareportal-2025-social"],
               "Instagram, YouTube and Facebook are huge; WhatsApp Status / channels are also a social surface. TikTok is strong.",
               "Instagram、YouTube、Facebook 體量很大；WhatsApp 狀態／頻道也是社交場域。TikTok 很強。", 2025),
    messaging=cat(["whatsapp"], ["telegram", "messenger"],
                  ["similarweb-messaging-2025", "datareportal-2025-brazil"],
                  "WhatsApp is the national default chat, culturally and in industry measurements.",
                  "無論在文化上還是行業測量中，WhatsApp 都是全國預設聊天工具。", 2025),
    payments=cat(["pix"], ["cards", "mercadopago"],
                 ["gsma-sotir-2026", "worldpay-gpr-2026"],
                 "Pix, the central bank’s instant rail, is the distinctive everyday payment layer. GSMA’s 2026 mobile-money report cites extremely high adult adoption in 2024. Cards and Mercado Pago remain in the mix. Colour payments as Pix.",
                 "中央銀行的即時軌道 Pix 是具特色的日常支付層。GSMA 2026 流動金錢報告引用 2024 年極高的成年使用率。卡與 Mercado Pago 仍在組合之中。支付層以 Pix 上色。", 2024),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("The showcase WhatsApp–Meta + Pix country: a global messaging default with a national instant-payment soul.",
            "WhatsApp／Meta＋Pix 的示範國家：全球級的預設通訊，再加上國家即時支付的靈魂。"),
))

for iso, iso3, en, zh, conf in [
    ("AR","ARG","Argentina","阿根廷","high"),
    ("CL","CHL","Chile","智利","high"),
    ("CO","COL","Colombia","哥倫比亞","high"),
    ("PE","PER","Peru","秘魯","high"),
    ("VE","VEN","Venezuela","委內瑞拉","low"),
    ("EC","ECU","Ecuador","厄瓜多爾","medium"),
    ("BO","BOL","Bolivia","玻利維亞","medium"),
    ("PY","PRY","Paraguay","巴拉圭","medium"),
    ("UY","URY","Uruguay","烏拉圭","medium"),
]:
    countries.append(C(
        iso=iso, iso3=iso3, name=N(en, zh),
        continent="South America", region="south-america", stack="whatsapp-meta",
        year=2025, confidence=conf,
        social=cat(["instagram", "facebook", "youtube"], ["tiktok"],
                   ["datareportal-country-index", "datareportal-2025-brazil"],
                   "Instagram, Facebook and YouTube are the usual Southern Cone / Andean public layer, following the same pattern as Brazil’s open social mix.",
                   "南錐／安第斯通常以 Instagram、Facebook、YouTube 為公開層，格局接近巴西的開放社交組合。", 2025),
        messaging=cat(["whatsapp"], ["messenger", "telegram"],
                      ["similarweb-messaging-2025"],
                      "WhatsApp is the regional default across Spanish-speaking South America in Similarweb 2025.",
                      "Similarweb 2025 顯示，西班牙語南美以 WhatsApp 為區域預設。", 2025),
        payments=cat(["mercadopago", "cards"], ["paypal"],
                     ["worldpay-gpr-2026"],
                     "Mercado Pago and cards are the usual pair. Pix from Brazil is expanding regionally but is not treated as already dominant outside Brazil in this compile. Venezuela is data-poor / unstable.",
                     "通常是 Mercado Pago 與卡。巴西的 Pix 正在區域擴張，但本次彙編不把它當成巴西以外已經主導。委內瑞拉屬資料不足／不穩定。", 2025),
        search=SEARCH_GOOGLE,
        ai=AI_DEFAULT,
        notes=N("Spanish-speaking South American WhatsApp–Meta, with Mercado Pago rather than Pix as the local payment colour.",
                "西班牙語南美的 WhatsApp／Meta，本地支付色是 Mercado Pago 而不是 Pix。"),
    ))
