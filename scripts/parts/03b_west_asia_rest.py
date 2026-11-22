countries.append(C(
    iso="IR", iso3="IRN", name=N("Iran", "伊朗"),
    continent="Asia", region="western-asia", stack="unknown",
    year=2025, confidence="low",
    social=cat(["instagram"], ["telegram"],
               ["datareportal-country-index"],
               "Filtering, blocks and rapid app substitution make this a low-confidence, data-poor map. Instagram and Telegram have been important, but availability changes. The UI must show this caveat.",
               "過濾、封鎖與 App 快速替換令此地圖信心低、資料不足。Instagram 與 Telegram 曾經重要，但可用性會變。介面必須顯示此保留。", 2025),
    messaging=cat(["telegram"], ["whatsapp"],
                  ["similarweb-messaging-2025"],
                  "Telegram has often been the practical default, subject to access restrictions. Low confidence.",
                  "在可使用時，Telegram 往往是實際上的預設，但受訪問限制影響。信心低。", 2025),
    payments=cat(["cards"], [], ["worldpay-gpr-2026"],
                 "Domestic bank cards and local apps; international wallets are a poor guide. Data-poor.",
                 "國內銀行卡與本地 App；國際錢包不是好的指南。資料不足。", 2025),
    search=cat(["google"], [], ["statcounter-search"],
               "Access to global search varies; do not treat a referral panel as a complete picture.",
               "全球搜尋的可及性不穩定；不要把轉介面板當成全貌。", 2026),
    ai=cat([], [], ["openai-availability-2026"],
           "This country is not on OpenAI’s supported-countries list. No AI leader is assigned.",
           "此地不在 OpenAI 支援名單。不指定 AI 領導產品。", 2026),
    notes=N("Data-poor by design: restrictions make platform defaults unstable. Shown as unknown / low confidence.",
            "刻意標為資料不足：限制令平台預設不穩定。以 unknown／低信心顯示。"),
))

for iso, iso3, en, zh in [("IQ","IRQ","Iraq","伊拉克"),("JO","JOR","Jordan","約旦"),
                          ("LB","LBN","Lebanon","黎巴嫩"),("PS","PSE","Palestine","巴勒斯坦"),
                          ("YE","YEM","Yemen","也門")]:
    countries.append(C(
        iso=iso, iso3=iso3, name=N(en, zh),
        continent="Asia", region="western-asia", stack="whatsapp-meta",
        year=2025, confidence="low" if iso in {"YE", "PS"} else "medium",
        social=cat(["facebook", "instagram"], ["youtube", "tiktok"], ["datareportal-country-index"],
                   "Facebook and Instagram are the usual public layer in regional accounts. Confidence is limited where connectivity or conflict disrupts measurement.",
                   "區域描述通常以 Facebook 與 Instagram 為公開層。在連線或衝突干擾測量的地方，信心有限。", 2025),
        messaging=cat(["whatsapp"], ["messenger", "telegram"], ["similarweb-messaging-2025"],
                      "WhatsApp is the regional default where measured.",
                      "在有測量的地方，區域預設為 WhatsApp。", 2025),
        payments=cat(["cards"], [], ["worldpay-gpr-2026"],
                     "No single national rail assigned.", "不指定單一國家軌道。", 2025),
        search=SEARCH_GOOGLE,
        ai=AI_DEFAULT,
        notes=N("Levant / Arabian WhatsApp–Meta pattern with uneven data quality.",
                "黎凡特／阿拉伯半島的 WhatsApp／Meta 格局，數據品質不均。"),
    ))

for iso, iso3, en, zh in [("GE","GEO","Georgia","格魯吉亞"),("AM","ARM","Armenia","亞美尼亞"),("AZ","AZE","Azerbaijan","阿塞拜疆"),("CY","CYP","Cyprus","塞浦路斯")]:
    if iso == "GE":
        messaging = cat(["messenger"], ["whatsapp"], ["similarweb-messaging-2025"],
                        "Older compilations often placed Messenger first in Georgia; treat as mixed / medium confidence.",
                        "較舊彙編常把喬治亞的 Messenger 列為首位；視為混合／中等信心。", 2025)
    else:
        messaging = cat(["whatsapp"], ["messenger", "telegram"], ["similarweb-messaging-2025"],
                        "WhatsApp is typical; some Caucasus markets still show strong Messenger use in older compilations.",
                        "一般是 WhatsApp；較舊的彙編中，部分高加索市場的 Messenger 仍然很強。", 2025)
    countries.append(C(
        iso=iso, iso3=iso3, name=N(en, zh),
        continent="Asia", region="western-asia", stack="whatsapp-meta",
        year=2025, confidence="medium",
        social=cat(["facebook", "instagram"], ["youtube"], ["datareportal-country-index"],
                   "Facebook and Instagram are the usual public feeds.",
                   "通常以 Facebook 與 Instagram 為公開動態。", 2025),
        messaging=messaging,
        payments=cat(["cards"], [], ["worldpay-gpr-2026"],
                     "Card and bank-app markets; no distinctive rail assigned.",
                     "卡與銀行 App 市場；不指定特色軌道。", 2025),
        search=SEARCH_GOOGLE,
        ai=AI_DEFAULT,
        notes=N("Smaller Western Asian markets on a WhatsApp/Meta pattern.", "較小的西亞市場，屬 WhatsApp／Meta 格局。"),
    ))
