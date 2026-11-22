# Nordics and Baltics
countries.append(eur("SE","SWE","Sweden","瑞典","northern-europe",
                     (["whatsapp", "signal"], ["messenger"],
                      "Similarweb 2025 flags Signal as number one in Sweden on Android; WhatsApp and Messenger remain widely used. Treat as mixed, not a Signal-only country.",
                      "Similarweb 2025 的 Android 排名將瑞典的 Signal 列為首位；WhatsApp 與 Messenger 仍然常用。視為混合，不是只有 Signal 的國家。"),
                     ["swish"], ["cards", "applepay"],
                     "Swish is the distinctive national P2P / everyday payment app sitting on the bank system.",
                     "Swish 是建立在銀行體系上、具特色的全國 P2P／日常支付 App。",
                     confidence="medium",
                     extra_notes=N("Swish is the payment signature; messaging is mixed.",
                                   "支付簽名是 Swish；通訊則是混合。")))
countries.append(eur("NO","NOR","Norway","挪威","northern-europe",
                     (["whatsapp", "messenger"], ["imessage"],
                      "Messenger has historically been strong in the Nordics; WhatsApp has grown. Treat as mixed.",
                      "北歐歷史上 Messenger 很強；WhatsApp 在增長。視為混合。"),
                     ["vipps"], ["cards", "applepay"],
                     "Vipps (now in the Vipps MobilePay family) is the distinctive national app.",
                     "Vipps（現屬 Vipps MobilePay 家族）是具特色的全國 App。",
                     confidence="medium"))
countries.append(eur("DK","DNK","Denmark","丹麥","northern-europe",
                     (["whatsapp", "messenger"], ["imessage"],
                      "Mixed Messenger / WhatsApp usage, typical of the Nordics.",
                      "Messenger／WhatsApp 混合，屬北歐典型。"),
                     ["vipps"], ["cards", "applepay"],
                     "MobilePay, now in the Vipps MobilePay family, is the distinctive national app.",
                     "MobilePay（現屬 Vipps MobilePay 家族）是具特色的全國 App。",
                     confidence="medium"))
countries.append(eur("FI","FIN","Finland","芬蘭","northern-europe",
                     (["whatsapp"], ["messenger", "signal"],
                      "WhatsApp is widely reported as strong in Finland; Signal appears as a secondary in some rankings.",
                      "多數描述指芬蘭的 WhatsApp 很強；部分排名中 Signal 是次選。"),
                     ["vipps"], ["cards"],
                     "MobilePay / Vipps MobilePay is the regional Nordic app of record; cards remain important.",
                     "MobilePay／Vipps MobilePay 是北歐地區的代表 App；卡仍然重要。",
                     confidence="medium"))
countries.append(eur("IS","ISL","Iceland","冰島","northern-europe",
                     (["whatsapp"], ["messenger"],
                      "Small market; WhatsApp / Messenger mix, medium-low confidence.",
                      "細小市場；WhatsApp／Messenger 混合，信心中低。"),
                     ["cards"], ["applepay"],
                     "Card-centric; no distinctive rail assigned.",
                     "偏卡；不指定特色軌道。", confidence="low"))

for iso, iso3, en, zh in [("EE","EST","Estonia","愛沙尼亞"),("LV","LVA","Latvia","拉脫維亞"),("LT","LTU","Lithuania","立陶宛")]:
    countries.append(eur(iso, iso3, en, zh, "northern-europe", WA,
                         ["cards"], ["applepay"],
                         "Bank-app and card markets in a highly digital Baltic setting; no single consumer wallet is painted as a monopoly.",
                         "高度數碼化的波羅的海環境中，以銀行 App 與卡為主；不把單一消費錢包畫成壟斷。",
                         confidence="medium"))

# Southern Europe
countries.append(eur("ES","ESP","Spain","西班牙","southern-europe", WA,
                     ["bizum", "cards"], ["applepay", "paypal"],
                     "Bizum is the distinctive bank P2P / checkout layer; cards remain central in store.",
                     "Bizum 是具特色的銀行 P2P／結帳層；店內仍以卡為核心。",
                     extra_notes=N("WhatsApp country with Bizum as the payment signature.",
                                   "WhatsApp 國家，支付簽名是 Bizum。")))
countries.append(eur("PT","PRT","Portugal","葡萄牙","southern-europe", WA,
                     ["mbway", "cards"], ["applepay"],
                     "MB WAY is the distinctive national wallet / P2P layer on top of cards.",
                     "MB WAY 是建立在卡之上、具特色的全國錢包／P2P 層。"))
countries.append(eur("IT","ITA","Italy","意大利","southern-europe", WA,
                     ["cards", "applepay"], ["paypal"],
                     "Cards and contactless wallets; no single Pix-like rail is assigned.",
                     "卡與感應錢包；不指定類似 Pix 的單一軌道。"))
countries.append(eur("GR","GRC","Greece","希臘","southern-europe", WA,
                     ["cards"], ["applepay"],
                     "Card-centric; IRIS and other bank rails exist but are not coloured as a monopoly in this compile.",
                     "偏卡；有 IRIS 等銀行軌道，但本次彙編不以壟斷上色。", confidence="medium"))
countries.append(eur("MT","MLT","Malta","馬耳他","southern-europe", WA,
                     ["cards"], [], "Small card-centric market.", "細小、偏卡的市場。", confidence="low"))
