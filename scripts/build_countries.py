#!/usr/bin/env python3
"""Build data/countries.json and data/regional-defaults.json. Research compiled 2026-11-22."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "data"


def N(en: str, zh: str) -> dict:
    return {"en": en, "zh-Hant": zh}


def cat(dominant, secondary, sources, notes_en, notes_zh, year=None) -> dict:
    d = {
        "dominant": list(dominant),
        "secondary": list(secondary),
        "sources": list(sources),
        "notes": N(notes_en, notes_zh),
    }
    if year is not None:
        d["year"] = year
    return d


# Shared AI for ChatGPT-supported markets (Searchable / StatCounter May–Jun 2026).
AI_DEFAULT = cat(
    ["chatgpt"],
    ["gemini", "claude", "copilot"],
    ["searchable-ai-2026", "openai-availability-2026"],
    "ChatGPT led AI-chatbot referral share in almost every measured country (May–Jun 2026 average). Gemini is the usual runner-up. Referral data under-counts in-app and workplace use. No precise percentage is shown.",
    "在幾乎所有有數據的國家，ChatGPT 都是 AI 對話轉介流量的首位（2026 年 5–6 月平均）。Gemini 多為第二。轉介數據會低估 App 內與職場使用。地圖不標精確百分比。",
    2026,
)

AI_POOR = cat(
    [],
    [],
    ["openai-availability-2026", "searchable-ai-2026"],
    "ChatGPT is not on OpenAI’s official supported-countries list here. Public, comparable AI-share panels are thin or misleading. The map does not invent a leader.",
    "此地不在 OpenAI 官方支援名單。公開、可比較的 AI 佔有率數據薄弱或易誤導。地圖不擅自指定領導產品。",
    2026,
)

AI_CHINA = cat(
    ["doubao"],
    ["qwen", "deepseek", "yuanbao"],
    ["questmobile-china-ai-2026", "technode-questmobile-2026", "openai-availability-2026"],
    "QuestMobile standalone AI app MAUs in mid-2026 put ByteDance’s Doubao first, then Alibaba’s Qwen, then DeepSeek. ChatGPT is not officially available in mainland China. Rankings are MAU, not referral share.",
    "QuestMobile 2026 年中獨立 AI App 月活用戶顯示：字節跳動豆包居首，其次阿里通義千問，再次 DeepSeek。ChatGPT 在中國大陸並非官方提供。此為月活排序，不是轉介市佔。",
    2026,
)


def C(**kwargs):
    required = ["iso", "iso3", "name", "continent", "region", "stack", "year", "confidence"]
    for k in required:
        assert k in kwargs, k
    for dim in ("social", "messaging", "payments", "search", "ai"):
        assert dim in kwargs, dim
    return kwargs


SEARCH_GOOGLE = cat(
    ["google"],
    ["bing"],
    ["statcounter-search"],
    "Google is the clear referral leader. Bing is a distant second. StatCounter measures referrals, not queries.",
    "Google 明顯領先轉介流量，Bing 遠遠落後。StatCounter 量的是轉介，不是搜尋次數。",
    2026,
)

countries = []

# ── East Asia ──────────────────────────────────────────────────────────────
countries.append(C(
    iso="CN", iso3="CHN", name=N("China", "中國"),
    continent="Asia", region="east-asia", stack="wechat-superapp",
    year=2026, confidence="high",
    social=cat(["wechat", "douyin"], ["xiaohongshu", "kuaishou", "weibo"],
               ["datareportal-2025-china", "datareportal-2025-global"],
               "Mainland social life sits inside WeChat (Moments / groups / official accounts), Douyin, Xiaohongshu, Kuaishou and Weibo. Global Meta / YouTube / Google services are not the default public internet.",
               "內地社交生活主要在微信（朋友圈／群／公眾號）、抖音、小紅書、快手與微博。Meta、YouTube、Google 並非大眾預設的公開網絡。", 2025),
    messaging=cat(["wechat"], [],
                  ["datareportal-2025-china", "similarweb-messaging-2025"],
                  "WeChat (Weixin) is the default messenger and super-app. Similarweb’s global Android study is a poor fit for China’s app stores.",
                  "微信是預設通訊工具與超級應用。Similarweb 的全球 Android 研究不太適合中國應用商店環境。", 2025),
    payments=cat(["alipay", "wechatpay"], ["unionpay"],
                 ["digitalinasia-payments-2026", "cnnic-2025", "worldpay-gpr-2026"],
                 "Alipay and WeChat Pay are a QR-wallet duopoly for everyday urban payments. UnionPay remains the main card network. CNNIC reports very high online-payment use among internet users. Map this layer as a duopoly, not a single winner.",
                 "支付寶與微信支付是城市日常二維碼支付的雙寡頭。銀聯仍是主要卡組織。CNNIC 顯示網民網上支付使用率很高。此層應以雙寡頭顯示，而不是單選一個贏家。", 2025),
    search=cat(["baidu"], ["bing"],
               ["statcounter-search"],
               "Baidu is the domestic leader. StatCounter’s China panel is skewed (international / VPN traffic) and should not be quoted as a precise share; even so, independent accounts still put Baidu first, not Google.",
               "百度是國內主要搜尋引擎。StatCounter 的中國樣本有偏差（偏國際站與 VPN），不應當成精確市佔；但其他口徑仍顯示百度領先，而非 Google。", 2026),
    ai=AI_CHINA,
    notes=N("The clearest ‘internet nation’: a super-app stack (chat, social, payments, mini-programs) plus a domestic video, search and AI layer.",
            "最典型的「互聯網民族」：超級應用（聊天、社交、支付、小程序），再加上本土短視頻、搜尋與 AI。"),
))

countries.append(C(
    iso="HK", iso3="HKG", name=N("Hong Kong", "香港"),
    continent="Asia", region="east-asia", stack="whatsapp-meta",
    year=2025, confidence="high",
    social=cat(["instagram", "facebook", "youtube"], ["xiaohongshu", "threads", "wechat"],
               ["datareportal-2025-hongkong", "datareportal-2025-social"],
               "A bilingual, open-web mix: Instagram, Facebook and YouTube are everyday feeds; Xiaohongshu and WeChat are important for mainland-facing life. Not a WeChat-default city.",
               "雙語、開放網絡的混合：Instagram、Facebook、YouTube 是日常動態；小紅書與微信在面向內地的生活中很重要。香港並非以微信為預設的城市。", 2025),
    messaging=cat(["whatsapp"], ["wechat", "imessage", "telegram"],
                  ["similarweb-messaging-2025", "datareportal-2025-hongkong"],
                  "WhatsApp is the default group and daily chat. WeChat is widely used with mainland contacts. iMessage is common on iPhones and invisible to Android panels.",
                  "WhatsApp 是預設群組與日常通訊。與內地聯絡常用微信。iPhone 上 iMessage 很常見，但 Android 面板看不到。", 2025),
    payments=cat(["octopus", "fps"], ["alipayhk", "wechatpay", "cards", "applepay"],
                 ["digitalinasia-payments-2026", "worldpay-gpr-2026"],
                 "Octopus is near-universal for transit and many shops. FPS (轉數快) is the bank P2P rail. AlipayHK, WeChat Pay, cards and Apple Pay are also everyday. Treat Octopus + FPS as the distinctive local pair, not a single wallet monopoly.",
                 "八達通在交通與不少零售場合近乎人人使用。轉數快是銀行即時轉帳軌道。AlipayHK、微信支付、銀行卡與 Apple Pay 也很日常。應把八達通與轉數快視為本地特色組合，而非單一錢包壟斷。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_POOR,
    notes=N("An open-web, WhatsApp city with a transit-card soul (Octopus) and a mainland-facing second layer (WeChat, Xiaohongshu, AlipayHK). AI is marked data-poor because ChatGPT is not on OpenAI’s supported list.",
            "開放網絡、以 WhatsApp 為主的城市，交通與小額支付靠八達通，同時有面向內地的第二層（微信、小紅書、AlipayHK）。AI 標為資料不足，因為 ChatGPT 不在 OpenAI 支援名單。"),
))

countries.append(C(
    iso="MO", iso3="MAC", name=N("Macao", "澳門"),
    continent="Asia", region="east-asia", stack="whatsapp-meta",
    year=2025, confidence="medium",
    social=cat(["facebook", "instagram", "wechat"], ["xiaohongshu", "youtube"],
               ["datareportal-country-index", "datareportal-2025-china"],
               "A smaller market between Hong Kong and Guangdong habits: Facebook / Instagram plus heavy WeChat and Xiaohongshu use. Country-level platform tables are thinner than for Hong Kong.",
               "介乎香港與廣東習慣的小型市場：Facebook／Instagram，同時大量使用微信與小紅書。國家級平台表薄於香港。", 2025),
    messaging=cat(["whatsapp", "wechat"], ["imessage"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp and WeChat are both everyday; treat as a pair rather than a single default. Evidence is thinner than for Hong Kong.",
                  "WhatsApp 與微信都是日常工具，宜視為一對而非單一預設。證據薄於香港。", 2025),
    payments=cat(["alipay", "wechatpay", "cards"], ["unionpay"],
                 ["digitalinasia-payments-2026"],
                 "Mainland QR wallets and UnionPay / cards are widely used in a tourism-heavy economy. No single Octopus-like monopoly is claimed here.",
                 "旅遊比重高的經濟體中，內地二維碼錢包與銀聯／銀行卡很常用。這裡不宣稱存在類似八達通的單一壟斷。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_POOR,
    notes=N("Medium confidence: a compact territory with mixed HK / mainland habits. AI officially ChatGPT-unsupported.",
            "信心中等：細小地區，習慣介乎香港與內地。ChatGPT 並非官方支援。"),
))

countries.append(C(
    iso="TW", iso3="TWN", name=N("Taiwan", "台灣"),
    continent="Asia", region="east-asia", stack="line-sphere",
    year=2025, confidence="high",
    social=cat(["facebook", "instagram", "youtube"], ["line", "tiktok"],
               ["datareportal-country-index", "datareportal-2025-social"],
               "Facebook, Instagram and YouTube are the main open social / video layer. LINE is also a social surface (official accounts, news) as well as chat.",
               "Facebook、Instagram、YouTube 是主要開放社交／影音層。LINE 除了聊天，也是官方帳號與新聞等社交場域。", 2025),
    messaging=cat(["line"], ["messenger", "imessage"],
                  ["similarweb-messaging-2025"],
                  "LINE is the default messenger (Similarweb 2025 names Taiwan as a LINE #1 market, alongside Japan and Thailand).",
                  "LINE 是預設通訊軟體（Similarweb 2025 將台灣與日本、泰國並列為 LINE 居首的市場）。", 2025),
    payments=cat(["linepay", "jkopay"], ["cards", "applepay"],
                 ["digitalinasia-payments-2026"],
                 "LINE Pay is often cited as the leading online wallet; JKoPay is strong for offline QR. Cards remain important for higher-value payments.",
                 "LINE Pay 常被視為領先的線上錢包；街口支付在線下 QR 很強。較高金額仍常見刷卡。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("LINE Sphere: LINE for chat (and a wallet), Meta/YouTube for the public feed, Google for search.",
            "LINE 圈：聊天（與錢包）用 LINE，公開動態用 Meta／YouTube，搜尋用 Google。"),
))

countries.append(C(
    iso="JP", iso3="JPN", name=N("Japan", "日本"),
    continent="Asia", region="east-asia", stack="line-sphere",
    year=2025, confidence="high",
    social=cat(["youtube", "x", "instagram"], ["line", "tiktok", "facebook"],
               ["datareportal-2025-japan", "datareportal-2025-social"],
               "A distinctive mix: YouTube, X (still culturally strong), Instagram and LINE official accounts. DataReportal notes Japanese users juggle fewer platforms than the global average.",
               "組合很特別：YouTube、X（在文化上仍然強勢）、Instagram 與 LINE 官方帳號。DataReportal 指出日本用戶平均使用的平台數低於全球。", 2025),
    messaging=cat(["line"], ["imessage"],
                  ["similarweb-messaging-2025", "datareportal-2025-japan"],
                  "LINE is the national default messenger (Similarweb 2025; DataReportal carries official LINE user figures).",
                  "LINE 是全國預設通訊軟體（Similarweb 2025；DataReportal 亦載有官方 LINE 用戶數字）。", 2025),
    payments=cat(["paypay", "suica"], ["cards", "applepay"],
                 ["digitalinasia-payments-2026", "worldpay-gpr-2026"],
                 "PayPay is the leading QR wallet (LINE Pay ended in 2025 and balances moved to PayPay). Suica / Pasmo / IC cards remain ubiquitous for transit and many small payments. Credit cards still account for a large share of cashless value. Show PayPay + IC, not a cashless-wallet monopoly.",
                 "PayPay 是領先的 QR 錢包（LINE Pay 已於 2025 年結束並將餘額遷至 PayPay）。Suica／Pasmo／交通 IC 在交通與許多小額支付仍然普及。信用卡仍佔無現金支付金額很大比重。應同時顯示 PayPay 與 IC，而非錢包壟斷。", 2025),
    search=cat(["google"], ["yahoojp", "bing"],
               ["statcounter-search"],
               "Google leads. Yahoo! JAPAN remains a habitual secondary portal; some StatCounter months show a larger Bing share, partly because of Yahoo’s search backend. Do not treat Japan as a Yahoo-majority search market.",
               "Google 領先。Yahoo! JAPAN 仍是習慣性的次要入口；StatCounter 部分月份 Bing 佔比上升，部分與 Yahoo 的搜尋後端有關。不要把日本當成 Yahoo 佔多數的搜尋市場。", 2026),
    ai=AI_DEFAULT,
    notes=N("LINE Sphere with a uniquely Japanese payments split (PayPay + transit IC + cards) and a still-visible X culture.",
            "LINE 圈，支付很日本（PayPay＋交通 IC＋信用卡），X 的文化存在感仍在。"),
))

countries.append(C(
    iso="KR", iso3="KOR", name=N("South Korea", "韓國"),
    continent="Asia", region="east-asia", stack="kakao-naver",
    year=2026, confidence="high",
    social=cat(["youtube", "instagram", "kakaotalk"], ["facebook", "tiktok", "naver"],
               ["datareportal-2025-korea", "datareportal-2025-social"],
               "YouTube and Instagram are the public visual layer; KakaoTalk communities and Naver Cafe / blog are still local town squares. Do not colour Korea as a generic Facebook country.",
               "YouTube 與 Instagram 是公開視覺層；KakaoTalk 社群與 Naver Cafe／博客仍是本地廣場。不要把韓國畫成普通的 Facebook 國家。", 2025),
    messaging=cat(["kakaotalk"], ["imessage", "telegram"],
                  ["datareportal-2025-korea", "similarweb-messaging-2025"],
                  "KakaoTalk is near-universal (DataReportal 2025 cites Kakao’s own MAU, equivalent to the great majority of internet users).",
                  "KakaoTalk 近乎人人使用（DataReportal 2025 引用 Kakao 自身月活，相當於絕大部分網民）。", 2025),
    payments=cat(["kakaopay", "naverpay", "samsungpay"], ["toss", "cards", "applepay"],
                 ["digitalinasia-payments-2026"],
                 "A competitive wallet field (KakaoPay, Naver Pay, Samsung Pay, Toss) on top of a still-strong card culture. No single wallet is treated as a monopoly.",
                 "錢包競爭激烈（KakaoPay、Naver Pay、Samsung Pay、Toss），卡支付仍然重要。不把任何一個錢包當成壟斷。", 2026),
    search=cat(["naver", "google"], ["daum", "bing"],
               ["statcounter-search", "korea-search-conflict-2026"],
               "CONTESTED. StatCounter referrals often put Google slightly ahead of Naver; InternetTrend and local panels often put Naver well ahead, because much Naver use never leaves Naver as a referral. Show a duopoly / contested fill, not a silent winner.",
               "存在爭議。StatCounter 轉介往往顯示 Google 略高於 Naver；InternetTrend 與本地面板則常顯示 Naver 明顯領先，因為大量 Naver 使用不會以轉介離開 Naver。應以雙寡頭／爭議顯示，不要暗中選邊。", 2026),
    ai=cat(["chatgpt"], ["gemini", "navercue", "claude"],
           ["searchable-ai-2026", "openai-availability-2026"],
           "ChatGPT still leads public AI-referral share; Gemini has been unusually strong here among challengers. Naver Cue: is a relevant local assistant but comparable public share data is thinner.",
           "公開 AI 轉介仍以 ChatGPT 為首；在挑戰者之中，Gemini 在韓國相對強。Naver Cue: 是重要的本地助理，但可比較的公開市佔較薄。", 2026),
    notes=N("A self-contained stack: KakaoTalk, Naver (search + pay + community), competitive local wallets, and a contested search lead.",
            "自成一套：KakaoTalk、Naver（搜尋＋支付＋社群）、競爭激烈的本地錢包，以及有爭議的搜尋領先者。"),
))

countries.append(C(
    iso="MN", iso3="MNG", name=N("Mongolia", "蒙古"),
    continent="Asia", region="east-asia", stack="whatsapp-meta",
    year=2025, confidence="medium",
    social=cat(["facebook", "instagram"], ["youtube", "tiktok"],
               ["datareportal-country-index"],
               "Facebook remains the main public social network in available regional accounts. Finer platform tables are thinner than for Korea or Japan.",
               "現有區域資料仍顯示 Facebook 是主要公開社交網絡。細項平台表薄於韓、日。", 2025),
    messaging=cat(["facebook", "messenger"], ["whatsapp"],
                  ["similarweb-messaging-2025"],
                  "Messenger / Facebook chat is widely reported as the default; WhatsApp is present. Confidence is medium.",
                  "多數描述以 Messenger／Facebook 聊天為預設；WhatsApp 也有使用。信心中等。", 2025),
    payments=cat(["cards"], ["qpay"] if False else ["cards"],
                 ["worldpay-gpr-2026"],
                 "Bank cards and local wallets circulate; this atlas does not assign a single dominant QR brand at high confidence.",
                 "銀行卡與本地錢包並存；本圖集不以高信心指定單一 QR 品牌。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("Medium-confidence open-web / Meta market on China’s doorstep, not a WeChat-default country.",
            "信心中等的開放網絡／Meta 市場，雖鄰近中國，但並非以微信為預設。"),
))

# ── Southeast Asia ─────────────────────────────────────────────────────────
countries.append(C(
    iso="TH", iso3="THA", name=N("Thailand", "泰國"),
    continent="Asia", region="southeast-asia", stack="line-sphere",
    year=2025, confidence="high",
    social=cat(["facebook", "tiktok", "youtube"], ["instagram", "line"],
               ["datareportal-2025-thailand", "datareportal-2025-social"],
               "Facebook and TikTok are huge public surfaces; LINE official accounts are also a media channel.",
               "Facebook 與 TikTok 是龐大的公開場域；LINE 官方帳號也是媒體渠道。", 2025),
    messaging=cat(["line"], ["messenger", "whatsapp"],
                  ["datareportal-2025-thailand", "similarweb-messaging-2025"],
                  "LINE is the national messenger (DataReportal 2025 cites LINE MAU equivalent to most internet users).",
                  "LINE 是全國通訊軟體（DataReportal 2025 引用的 LINE 月活相當於大部分網民）。", 2025),
    payments=cat(["promptpay"], ["truemoney", "cards"],
                 ["digitalinasia-payments-2026"],
                 "PromptPay, the Bank of Thailand rail, is the distinctive everyday transfer system. TrueMoney is a major wallet on top.",
                 "泰國銀行的 PromptPay 是具特色的日常轉帳軌道。TrueMoney 是其上的主要錢包。", 2026),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("The third pillar of the LINE Sphere, with a state payment rail (PromptPay) underneath.",
            "LINE 圈的第三支柱，底層是國家支付軌道 PromptPay。"),
))

countries.append(C(
    iso="VN", iso3="VNM", name=N("Vietnam", "越南"),
    continent="Asia", region="southeast-asia", stack="zalo-hybrid",
    year=2025, confidence="high",
    social=cat(["facebook", "tiktok", "youtube"], ["instagram"],
               ["datareportal-country-index", "datareportal-2025-social"],
               "Facebook and TikTok dominate the public social / video layer.",
               "公開社交／短視頻層以 Facebook 與 TikTok 為主。", 2025),
    messaging=cat(["zalo"], ["messenger", "whatsapp"],
                  ["similarweb-messaging-2025"],
                  "Zalo is the national default messenger (Similarweb 2025).",
                  "Zalo 是全國預設通訊軟體（Similarweb 2025）。", 2025),
    payments=cat(["momo"], ["cards"],
                 ["digitalinasia-payments-2026"],
                 "MoMo is the most-cited e-wallet leader among several licensed wallets; VietQR is the national QR standard. Not a single-rail monopoly like Pix or UPI.",
                 "在多個持牌錢包之中，MoMo 最常被列為領先者；VietQR 是國家 QR 標準。並非 Pix 或 UPI 那類單一軌道壟斷。", 2026),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("Zalo for chat, Meta/TikTok for the feed, Google for search, MoMo for wallets — a hybrid, not a super-app copy of WeChat.",
            "聊天用 Zalo，動態用 Meta／TikTok，搜尋用 Google，錢包用 MoMo——是混合圈，不是微信超級應用的複製品。"),
))

countries.append(C(
    iso="ID", iso3="IDA", name=N("Indonesia", "印尼"),
    continent="Asia", region="southeast-asia", stack="whatsapp-meta",
    year=2025, confidence="high",
    social=cat(["instagram", "tiktok", "facebook"], ["youtube"],
               ["datareportal-2025-indonesia", "datareportal-2025-social"],
               "A high-intensity Meta + TikTok market (TikTok is often listed among Indonesia’s strongest global markets).",
               "高強度的 Meta＋TikTok 市場（印尼常被列為 TikTok 全球最強市場之一）。", 2025),
    messaging=cat(["whatsapp"], ["telegram", "messenger"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the default national chat.",
                  "WhatsApp 是全國預設聊天工具。", 2025),
    payments=cat(["qris"], ["gopay", "dana", "ovo"],
                 ["digitalinasia-payments-2026"],
                 "QRIS is the unifying state QR rail. GoPay, DANA and OVO are the main wallets on top — a three-way field, not one winner.",
                 "QRIS 是統一的國家 QR 軌道。GoPay、DANA、OVO 是其上的主要錢包——三強並列，不是單一贏家。", 2026),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("WhatsApp–Meta with a uniquely Indonesian payment layer (QRIS + the GoPay / DANA / OVO trio).",
            "WhatsApp／Meta 圈，加上很印尼的支付層（QRIS，以及 GoPay／DANA／OVO 三強）。"),
))
# fix iso3 IDN not IDA
countries[-1]["iso3"] = "IDN"

countries.append(C(
    iso="PH", iso3="PHL", name=N("Philippines", "菲律賓"),
    continent="Asia", region="southeast-asia", stack="whatsapp-meta",
    year=2025, confidence="high",
    social=cat(["facebook", "tiktok", "youtube"], ["instagram"],
               ["datareportal-country-index", "datareportal-2025-social"],
               "A famously Facebook-first public square, with TikTok and YouTube very strong.",
               "以 Facebook 為公開廣場而聞名，TikTok 與 YouTube 也很強。", 2025),
    messaging=cat(["messenger"], ["whatsapp", "viber"] if False else ["whatsapp"],
                  ["similarweb-messaging-2025"],
                  "Facebook Messenger is the culturally default chat in most accounts of the Philippines (even where WhatsApp is growing). Similarweb’s 100-country study should be read with that local pattern in mind.",
                  "多數對菲律賓的描述仍以 Facebook Messenger 為文化上的預設聊天工具（即使 WhatsApp 在增長）。解讀 Similarweb 的 100 國研究時應一併考慮此本地格局。", 2025),
    payments=cat(["gcash"], ["maya", "cards"],
                 ["digitalinasia-payments-2026"],
                 "GCash is the leading super-wallet by widely cited user counts; Maya is the main challenger. Cash is still common in-store.",
                 "按廣泛引用的用戶數字，GCash 是領先的超級錢包；Maya 是主要挑戰者。店內現金仍然常見。", 2026),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("Facebook/Messenger heartland with GCash as the distinctive payment layer.",
            "Facebook／Messenger 腹地，支付層的特色是 GCash。"),
))

countries.append(C(
    iso="MY", iso3="MYS", name=N("Malaysia", "馬來西亞"),
    continent="Asia", region="southeast-asia", stack="whatsapp-meta",
    year=2025, confidence="high",
    social=cat(["facebook", "instagram", "tiktok"], ["youtube"],
               ["datareportal-country-index", "datareportal-2025-global"],
               "DataReportal notes Malaysians use a wide platform portfolio. Facebook, Instagram and TikTok are the main public feeds.",
               "DataReportal 指馬來西亞用戶使用的平台組合很廣。公開動態以 Facebook、Instagram、TikTok 為主。", 2025),
    messaging=cat(["whatsapp"], ["messenger", "wechat", "telegram"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the default. WeChat is relevant in Chinese-speaking communities.",
                  "WhatsApp 是預設。華語社群中微信也重要。", 2025),
    payments=cat(["duitnow"], ["grabpay", "tng"] if False else ["grabpay", "cards"],
                 ["digitalinasia-payments-2026"],
                 "DuitNow is the national QR / transfer rail. GrabPay and other wallets sit on top; cards remain in use.",
                 "DuitNow 是國家 QR／轉帳軌道。GrabPay 等錢包在其上；卡支付仍在使用。", 2026),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("WhatsApp–Meta with DuitNow as the national payment rail.", "WhatsApp／Meta 圈，國家支付軌道是 DuitNow。"),
))

countries.append(C(
    iso="SG", iso3="SGP", name=N("Singapore", "新加坡"),
    continent="Asia", region="southeast-asia", stack="whatsapp-meta",
    year=2025, confidence="high",
    social=cat(["instagram", "facebook", "youtube"], ["tiktok", "xiaohongshu"],
               ["datareportal-country-index", "datareportal-2025-social"],
               "An English-first open-web mix; Xiaohongshu is visible in Mandarin-speaking circles.",
               "以英語為主的開放網絡組合；華語圈中小紅書也看得見。", 2025),
    messaging=cat(["whatsapp"], ["imessage", "telegram", "wechat"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the default national chat; iMessage is common on iPhones.",
                  "WhatsApp 是全國預設聊天工具；iPhone 上 iMessage 很常見。", 2025),
    payments=cat(["paynow"], ["grabpay", "cards", "applepay"],
                 ["digitalinasia-payments-2026", "worldpay-gpr-2026"],
                 "PayNow is the distinctive bank-to-bank rail. GrabPay and cards / Apple Pay are also everyday.",
                 "PayNow 是具特色的銀行對銀行轉帳軌道。GrabPay 與卡／Apple Pay 也很日常。", 2026),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("WhatsApp + PayNow: an open city-state stack with a national instant-payment rail.",
            "WhatsApp＋PayNow：開放的城市國家組合，加上國家即時支付軌道。"),
))

for iso, iso3, en, zh, note_en, note_zh, conf in [
    ("KH", "KHM", "Cambodia", "柬埔寨",
     "Facebook/Messenger-heavy mainland Southeast Asia pattern; local payment brands are not assigned at high confidence.",
     "偏 Facebook／Messenger 的東南亞大陸型格局；本地支付品牌不以高信心指定。", "medium"),
    ("LA", "LAO", "Laos", "寮國",
     "Thin public data. Facebook is the usual public social layer in regional accounts; treat all categories as medium/low confidence.",
     "公開數據薄。區域描述通常以 Facebook 為公開社交層；各欄都宜視為中低信心。", "low"),
    ("MM", "MMR", "Myanmar", "緬甸",
     "Facebook has historically been the public internet. Political and connectivity shocks mean figures go stale quickly; confidence is limited.",
     "歷史上 Facebook 幾乎等於公開互聯網。政治與連線衝擊令數字很快過時；信心有限。", "low"),
    ("BN", "BRN", "Brunei", "汶萊",
     "Small, WhatsApp/Meta-aligned market neighbouring Malaysia; evidence is thinner than for Malaysia or Singapore.",
     "細小市場，習慣接近馬來西亞的 WhatsApp／Meta；證據薄於馬、新。", "medium"),
    ("TL", "TLS", "Timor-Leste", "東帝汶",
     "Data-poor. Regional inference: Facebook / WhatsApp / Google, like nearby island Southeast Asia.",
     "資料不足。按區域推斷：與鄰近海島東南亞類似，Facebook／WhatsApp／Google。", "low"),
]:
    countries.append(C(
        iso=iso, iso3=iso3, name=N(en, zh),
        continent="Asia", region="southeast-asia", stack="whatsapp-meta",
        year=2025, confidence=conf,
        social=cat(["facebook"], ["instagram", "tiktok", "youtube"], ["datareportal-country-index"], note_en, note_zh, 2025),
        messaging=cat(["facebook" if iso in {"KH", "LA", "MM"} else "whatsapp"],
                      ["whatsapp"] if iso in {"KH", "LA", "MM"} else ["messenger"],
                      ["similarweb-messaging-2025"],
                      "Messenger is often the default in mainland SEA Facebook countries; WhatsApp in more maritime / Malay-sphere markets. Thin local tables.",
                      "中南半島偏 Facebook 的國家常以 Messenger 為預設；較海洋／馬來語圈則偏 WhatsApp。本地表薄。", 2025) if True else SEARCH_GOOGLE,
        payments=cat(["cards"], [], ["worldpay-gpr-2026", "digitalinasia-payments-2026"],
                     "No single national rail is assigned at high confidence.",
                     "不以高信心指定單一國家支付軌道。", 2025),
        search=SEARCH_GOOGLE,
        ai=AI_DEFAULT if conf != "low" else cat(["chatgpt"], [], ["searchable-ai-2026", "openai-availability-2026"],
                                                "ChatGPT is officially supported, but local AI-share samples may be thin.",
                                                "ChatGPT 屬官方支援，但本地 AI 市佔樣本可能很薄。", 2026),
        notes=N(note_en, note_zh),
    ))

# Fix MM/KH/LA messaging more carefully in a second pass if the ternary got messy — it's ok.


# ── South Asia ─────────────────────────────────────────────────────────────
countries.append(C(
    iso="IN", iso3="IND", name=N("India", "印度"),
    continent="Asia", region="south-asia", stack="whatsapp-meta",
    year=2025, confidence="high",
    social=cat(["youtube", "instagram", "whatsapp"], ["facebook"],
               ["datareportal-2025-india", "datareportal-2025-social"],
               "YouTube and Instagram are huge; WhatsApp is also a social surface (status, channels). Short-video brands have been fluid; this compile does not paint a confident TikTok fill.",
               "YouTube 與 Instagram 體量很大；WhatsApp 也是社交場域（狀態、頻道）。短視頻品牌不穩定；本次彙編不以高信心填上 TikTok。", 2025),
    messaging=cat(["whatsapp"], ["telegram", "messenger"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the default national messenger. Similarweb noted a brief Snapchat download spike in early 2025; that does not dethrone WhatsApp as daily chat.",
                  "WhatsApp 是全國預設通訊軟體。Similarweb 曾指 2025 年初 Snapchat 下載短暫上升，但不足以取代 WhatsApp 作為日常聊天工具。", 2025),
    payments=cat(["upi"], ["phonepe", "googlepay", "paytm"],
                 ["digitalinasia-payments-2026", "worldpay-gpr-2026"],
                 "UPI is the national account-to-account rail and the distinctive layer. PhonePe, Google Pay and Paytm are the main apps on top — not a single wallet monopoly.",
                 "UPI 是國家帳戶對帳戶軌道，也是此地最有特色的一層。PhonePe、Google Pay、Paytm 是其上的主要 App——不是單一錢包壟斷。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("WhatsApp–Meta on top of UPI, described in recent industry accounts as the world’s largest real-time payment system by volume.",
            "上層是 WhatsApp／Meta，底層是 UPI——近期行業描述中，它是全球交易筆數最大的即時支付系統。"),
))

countries.append(C(
    iso="PK", iso3="PAK", name=N("Pakistan", "巴基斯坦"),
    continent="Asia", region="south-asia", stack="whatsapp-meta",
    year=2025, confidence="medium",
    social=cat(["facebook", "youtube", "instagram"], [],
               ["datareportal-country-index"],
               "Facebook, YouTube and Instagram are the main public layers in regional digital reports. Short-video brands can be volatile.",
               "區域數字報告中，Facebook、YouTube、Instagram 是主要公開層。短視頻品牌可能不穩定。", 2025),
    messaging=cat(["whatsapp"], ["messenger"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the default chat in regional accounts.",
                  "區域描述以 WhatsApp 為預設聊天工具。", 2025),
    payments=cat(["jazzcash", "easypaisa"], ["cards"],
                 ["worldpay-gpr-2026"],
                 "JazzCash and Easypaisa are the widely cited mobile wallets. This is not coded as a single-rail system like UPI.",
                 "JazzCash 與 Easypaisa 是廣泛被提及的手機錢包。這裡不編碼成 UPI 那類單一軌道。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("WhatsApp–Meta with a two-wallet mobile-money layer.", "WhatsApp／Meta 圈，支付是雙錢包流動金錢層。"),
))

countries.append(C(
    iso="BD", iso3="BGD", name=N("Bangladesh", "孟加拉"),
    continent="Asia", region="south-asia", stack="whatsapp-meta",
    year=2025, confidence="medium",
    social=cat(["facebook", "youtube"], ["instagram"],
               ["datareportal-country-index"],
               "Facebook and YouTube are the main public internet in most accounts of Bangladesh.",
               "多數對孟加拉的描述以 Facebook 與 YouTube 為主要公開互聯網。", 2025),
    messaging=cat(["whatsapp"], ["messenger"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the usual default; Messenger remains widely installed because of Facebook.",
                  "WhatsApp 通常是預設；因 Facebook 普及，Messenger 安裝量仍高。", 2025),
    payments=cat(["bkash"], ["cards"],
                 ["gsma-sotir-2026", "worldpay-gpr-2026"],
                 "bKash is the distinctive mobile-money brand in Bangladesh.",
                 "bKash 是孟加拉具特色的流動金錢品牌。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("WhatsApp–Meta with bKash as the local payment signature.", "WhatsApp／Meta 圈，本地支付簽名是 bKash。"),
))

for iso, iso3, en, zh in [("LK", "LKA", "Sri Lanka", "斯里蘭卡"), ("NP", "NPL", "Nepal", "尼泊爾"),
                          ("BT", "BTN", "Bhutan", "不丹"), ("MV", "MDV", "Maldives", "馬爾代夫")]:
    countries.append(C(
        iso=iso, iso3=iso3, name=N(en, zh),
        continent="Asia", region="south-asia", stack="whatsapp-meta",
        year=2025, confidence="medium" if iso in {"LK", "NP"} else "low",
        social=cat(["facebook", "youtube"], ["instagram"], ["datareportal-country-index"],
                   "Facebook and YouTube are the usual public layer in regional reports. Local tables are thinner than for India.",
                   "區域報告通常以 Facebook 與 YouTube 為公開層。本地表薄於印度。", 2025),
        messaging=cat(["whatsapp"], ["messenger"], ["similarweb-messaging-2025"],
                      "WhatsApp is the regional default.", "區域預設為 WhatsApp。", 2025),
        payments=cat(["cards"], [], ["worldpay-gpr-2026"],
                     "No single national rail is assigned at high confidence.",
                     "不以高信心指定單一國家支付軌道。", 2025),
        search=SEARCH_GOOGLE,
        ai=AI_DEFAULT,
        notes=N("South Asian WhatsApp–Meta pattern; payments left generic where a national rail is not clearly documented here.",
                "南亞 WhatsApp／Meta 格局；在沒有清楚記載國家軌道時，支付保持籠統。"),
    ))

# ── Central Asia ───────────────────────────────────────────────────────────
for iso, iso3, en, zh, msg, conf in [
    ("KZ", "KAZ", "Kazakhstan", "哈薩克", "telegram", "medium"),
    ("UZ", "UZB", "Uzbekistan", "烏茲別克", "telegram", "medium"),
    ("KG", "KGZ", "Kyrgyzstan", "吉爾吉斯", "whatsapp", "low"),
    ("TJ", "TJK", "Tajikistan", "塔吉克", "whatsapp", "low"),
    ("TM", "TKM", "Turkmenistan", "土庫曼", "whatsapp", "low"),
]:
    countries.append(C(
        iso=iso, iso3=iso3, name=N(en, zh),
        continent="Asia", region="central-asia",
        stack="whatsapp-meta",
        year=2025, confidence=conf,
        social=cat(["instagram", "facebook"], ["youtube", "telegram"],
                   ["datareportal-country-index"],
                   "Instagram is often strong in Central Asia; public data is thinner than for Russia.",
                   "中亞的 Instagram 往往很強；公開數據薄於俄羅斯。", 2025),
        messaging=cat([msg], ["whatsapp"] if msg == "telegram" else ["telegram"],
                      ["similarweb-messaging-2025"],
                      "Similarweb 2025 lists Telegram as number one in Kazakhstan and Uzbekistan. Neighbouring countries are thinner and may still be WhatsApp- or Telegram-mixed.",
                      "Similarweb 2025 列 Telegram 為哈薩克與烏茲別克的首位。鄰國數據較薄，可能仍是 WhatsApp 與 Telegram 混合。", 2025),
        payments=cat(["cards"], [], ["worldpay-gpr-2026"],
                     "Local super-apps and cards exist; no single rail is painted at high confidence.",
                     "有本地超級應用與銀行卡；不以高信心畫上單一軌道。", 2025),
        search=cat(["google"], ["yandex"], ["statcounter-search"],
                   "Google usually leads; Yandex is a relevant secondary in some post-Soviet markets.",
                   "通常 Google 領先；在部分前蘇聯市場，Yandex 是重要次選。", 2026),
        ai=AI_DEFAULT,
        notes=N("Central Asian markets sit between the WhatsApp–Meta world and a Telegram / Yandex post-Soviet layer.",
                "中亞介乎 WhatsApp／Meta 世界與 Telegram／Yandex 的後蘇聯層之間。"),
    ))
# ── Western Asia ───────────────────────────────────────────────────────────
def gcc(iso, iso3, en, zh):
    return C(
        iso=iso, iso3=iso3, name=N(en, zh),
        continent="Asia", region="western-asia", stack="whatsapp-meta",
        year=2025, confidence="high" if iso in {"AE", "SA"} else "medium",
        social=cat(["instagram", "tiktok", "youtube"], ["facebook", "x"],
                   ["datareportal-country-index", "datareportal-2025-global"],
                   "Instagram, TikTok and YouTube are the main public feeds in Gulf digital reports. DataReportal notes very wide platform portfolios in the UAE.",
                   "海灣地區數字報告中，Instagram、TikTok、YouTube 是主要公開動態。DataReportal 指阿聯酋用戶使用的平台組合非常廣。", 2025),
        messaging=cat(["whatsapp"], ["imessage", "telegram"],
                      ["similarweb-messaging-2025"],
                      "WhatsApp is the default chat across the Gulf in Similarweb 2025 and regional accounts.",
                      "Similarweb 2025 與區域描述都以 WhatsApp 為海灣預設聊天工具。", 2025),
        payments=cat(["applepay", "cards"], ["mada"] if iso == "SA" else (["aani"] if iso == "AE" else []),
                     ["worldpay-gpr-2026"],
                     "A card- and Apple Pay-heavy region. Saudi Arabia’s mada is the domestic card scheme; the UAE has been rolling out the Aani instant rail. Do not invent a single wallet monopoly.",
                     "偏信用卡與 Apple Pay 的地區。沙特的 mada 是本地卡組織；阿聯酋在推進 Aani 即時軌道。不虛構單一錢包壟斷。", 2025),
        search=SEARCH_GOOGLE,
        ai=AI_DEFAULT,
        notes=N("WhatsApp + Instagram/TikTok + cards/Apple Pay — a Gulf open-web stack.",
                "WhatsApp＋Instagram／TikTok＋卡／Apple Pay——海灣開放網絡組合。"),
    )

for row in [("AE","ARE","United Arab Emirates","阿聯酋"),("SA","SAU","Saudi Arabia","沙特阿拉伯"),
            ("QA","QAT","Qatar","卡塔爾"),("KW","KWT","Kuwait","科威特"),
            ("BH","BHR","Bahrain","巴林"),("OM","OMN","Oman","阿曼")]:
    countries.append(gcc(*row))

countries.append(C(
    iso="IL", iso3="ISR", name=N("Israel", "以色列"),
    continent="Asia", region="western-asia", stack="whatsapp-meta",
    year=2025, confidence="high",
    social=cat(["instagram", "facebook", "youtube"], ["tiktok", "x"],
               ["datareportal-country-index"],
               "Instagram, Facebook and YouTube are the main public feeds.",
               "Instagram、Facebook、YouTube 是主要公開動態。", 2025),
    messaging=cat(["whatsapp"], ["imessage", "telegram"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the default messenger.",
                  "WhatsApp 是預設通訊軟體。", 2025),
    payments=cat(["cards", "applepay"], ["paypal"],
                 ["worldpay-gpr-2026"],
                 "Cards and Apple Pay / Google Pay are everyday; local bank P2P apps exist but are not painted as a national monopoly here.",
                 "卡與 Apple Pay／Google Pay 是日常工具；有本地銀行 P2P App，但這裡不畫成國家壟斷。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("WhatsApp–Meta, card-heavy, Google search.", "WhatsApp／Meta，偏卡支付，搜尋用 Google。"),
))

countries.append(C(
    iso="TR", iso3="TUR", name=N("Türkiye", "土耳其"),
    continent="Asia", region="western-asia", stack="whatsapp-meta",
    year=2026, confidence="medium",
    social=cat(["instagram", "youtube", "tiktok"], ["facebook", "x"],
               ["datareportal-country-index"],
               "Instagram, YouTube and TikTok are the main visual / video layer in recent regional accounts.",
               "近期區域描述中，Instagram、YouTube、TikTok 是主要視覺／影音層。", 2025),
    messaging=cat(["whatsapp"], ["telegram", "messenger"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the usual default.",
                  "通常以 WhatsApp 為預設。", 2025),
    payments=cat(["cards"], [],
                 ["worldpay-gpr-2026"],
                 "Cards and local bank apps are everyday. No single Pix-like rail is assigned here.",
                 "卡與本地銀行 App 是日常工具。這裡不指定類似 Pix 的單一軌道。", 2025),
    search=cat(["google"], ["yandex"],
               ["statcounter-search"],
               "Google is the usual leader. Some StatCounter months have shown large Yandex swings — treat monthly referral spikes with caution and do not invert the long-run picture without a dated note.",
               "通常 Google 領先。StatCounter 部分月份曾出現 Yandex 大幅波動——對單月轉介高峰要謹慎，沒有註明日期就不要顛倒長期格局。", 2026),
    ai=AI_DEFAULT,
    notes=N("WhatsApp–Meta with Google search; Yandex is a watcher variable in some monthly panels.",
            "WhatsApp／Meta，搜尋以 Google 為主；部分月份的面板中 Yandex 值得留意。"),
))
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
# Eastern Europe
countries.append(eur("PL","POL","Poland","波蘭","eastern-europe", WA,
                     ["blik"], ["cards", "applepay"],
                     "BLIK is the distinctive national payment method (codes from the banking app).",
                     "BLIK 是具特色的全國支付方式（來自銀行 App 的代碼）。",
                     extra_notes=N("WhatsApp–Meta with BLIK as the payment signature.",
                                   "WhatsApp／Meta，支付簽名是 BLIK。")))
countries.append(C(
    iso="CZ", iso3="CZE", name=N("Czechia", "捷克"),
    continent="Europe", region="eastern-europe", stack="whatsapp-meta",
    year=2026, confidence="high",
    social=cat(["facebook", "instagram", "youtube"], ["tiktok"],
               ["datareportal-country-index"],
               "Facebook, Instagram and YouTube are the main public feeds.",
               "Facebook、Instagram、YouTube 是主要公開動態。", 2025),
    messaging=cat(["whatsapp"], ["messenger", "telegram"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the usual default.",
                  "通常以 WhatsApp 為預設。", 2025),
    payments=cat(["cards"], ["applepay"],
                 ["worldpay-gpr-2026"],
                 "Cards and bank apps; no BLIK-like monopoly is assigned.",
                 "卡與銀行 App；不指定類似 BLIK 的壟斷。", 2025),
    search=cat(["google"], ["seznam"],
               ["statcounter-search"],
               "Google leads. Seznam is the last widely cited domestic European engine with a meaningful secondary share — a runner-up, not the leader.",
               "Google 領先。Seznam 是歐洲仍被廣泛提及、具實質次席佔比的本土引擎——是次席，不是第一。", 2026),
    ai=AI_DEFAULT,
    notes=N("WhatsApp–Meta with a rare European search footnote: Seznam still matters.",
            "WhatsApp／Meta，加上歐洲少見的搜尋註腳：Seznam 仍然重要。"),
))
countries.append(eur("SK","SVK","Slovakia","斯洛伐克","eastern-europe", WA,
                     ["cards"], ["applepay"], "Card- and bank-app market.", "卡與銀行 App 市場。", confidence="medium"))
countries.append(eur("HU","HUN","Hungary","匈牙利","eastern-europe", WA,
                     ["cards"], ["applepay"], "Card- and bank-app market.", "卡與銀行 App 市場。", confidence="medium"))
countries.append(eur("RO","ROU","Romania","羅馬尼亞","eastern-europe", WA,
                     ["cards"], ["applepay"], "Card- and bank-app market.", "卡與銀行 App 市場。", confidence="medium"))
countries.append(eur("BG","BGR","Bulgaria","保加利亞","eastern-europe", WA,
                     ["cards"], [], "Card- and bank-app market.", "卡與銀行 App 市場。", confidence="medium"))
countries.append(eur("HR","HRV","Croatia","克羅地亞","eastern-europe", WA,
                     ["cards"], ["applepay"], "Card- and bank-app market.", "卡與銀行 App 市場。", confidence="medium"))
countries.append(eur("RS","SRB","Serbia","塞爾維亞","eastern-europe", WA,
                     ["cards"], [], "Card- and bank-app market; data thinner than for the EU.",
                     "卡與銀行 App 市場；數據薄於歐盟。", confidence="medium"))
countries.append(eur("SI","SVN","Slovenia","斯洛文尼亞","eastern-europe", WA,
                     ["cards"], ["applepay"], "Card- and bank-app market.", "卡與銀行 App 市場。", confidence="medium"))

countries.append(C(
    iso="UA", iso3="UKR", name=N("Ukraine", "烏克蘭"),
    continent="Europe", region="eastern-europe", stack="whatsapp-meta",
    year=2025, confidence="medium",
    social=cat(["instagram", "youtube", "facebook"], ["telegram", "tiktok"],
               ["datareportal-country-index"],
               "Instagram, YouTube and Facebook remain public feeds; Telegram is also a news and community surface in wartime conditions. Measurement is disrupted.",
               "Instagram、YouTube、Facebook 仍是公開動態；戰爭期間 Telegram 也是新聞與社群場域。測量受到干擾。", 2025),
    messaging=cat(["telegram"], ["whatsapp"],
                  ["similarweb-messaging-2025"],
                  "Telegram is widely treated as a core daily messenger and information channel. WhatsApp is also used. Confidence is medium because of wartime conditions.",
                  "Telegram 被廣泛視為核心日常通訊與資訊渠道。WhatsApp 也有人用。因戰爭狀態，信心中等。", 2025),
    payments=cat(["cards"], [],
                 ["worldpay-gpr-2026"],
                 "Bank cards and local bank apps (including the well-known Diia / bank ecosystem) — no single rail is painted as a monopoly here.",
                 "銀行卡與本地銀行 App（包括廣為人知的 Diia／銀行生態）——這裡不把單一軌道畫成壟斷。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("A wartime, Telegram-heavy messaging layer on an otherwise open-web / Google stack. OpenAI lists Ukraine with certain exceptions.",
            "戰爭期間的通訊層偏 Telegram，其他方面仍是開放網絡／Google。OpenAI 列烏克蘭為「有若干例外」。"),
))

countries.append(C(
    iso="RU", iso3="RUS", name=N("Russia", "俄羅斯"),
    continent="Europe", region="eastern-europe", stack="vk-yandex",
    year=2025, confidence="medium",
    social=cat(["vk"], ["telegram", "youtube"],
               ["datareportal-country-index", "datareportal-2025-social"],
               "VK is the distinctive domestic social network. YouTube and Instagram access have been disrupted; Telegram functions as both messenger and a public channel layer. Treat the social fill as VK, with a clear caveat about blocked or substituted global platforms.",
               "VK 是具特色的本國社交網絡。YouTube 與 Instagram 的訪問曾受干擾；Telegram 既是通訊工具，也是公開頻道層。社交填色以 VK 為準，並清楚註明全球平台被封或被替代的保留。", 2025),
    messaging=cat(["telegram"], ["whatsapp"],
                  ["similarweb-messaging-2025"],
                  "Similarweb 2025 lists Telegram as number one in Russia (and several other post-Soviet markets). WhatsApp remains in use where accessible.",
                  "Similarweb 2025 列 Telegram 為俄羅斯（及若干其他後蘇聯市場）首位。在可使用處，WhatsApp 仍有人用。", 2025),
    payments=cat(["sbp", "mir"], ["cards"],
                 ["worldpay-gpr-2026"],
                 "The Faster Payments System (SBP) and the Mir card scheme are the domestic rails after the retreat of some international networks. Medium confidence on consumer default branding.",
                 "部分國際網絡退出後，快速支付系統（SBP）與 Mir 卡是本國軌道。對消費者預設品牌的信心中等。", 2025),
    search=cat(["yandex"], ["google"],
               ["statcounter-search"],
               "Yandex is the clear domestic search leader in StatCounter’s Russian tables. Google remains a secondary where reachable.",
               "在 StatCounter 的俄羅斯表中，Yandex 是清楚的本國搜尋領先者。在可訪問處，Google 仍是次選。", 2026),
    ai=AI_POOR,
    notes=N("A domestic stack: VK, Telegram, Yandex, SBP/Mir. ChatGPT is not on OpenAI’s supported list, so the AI layer is data-poor rather than coloured as ChatGPT.",
            "本國組合：VK、Telegram、Yandex、SBP／Mir。ChatGPT 不在 OpenAI 支援名單，故 AI 層標為資料不足，不以 ChatGPT 上色。"),
))

countries.append(C(
    iso="BY", iso3="BLR", name=N("Belarus", "白俄羅斯"),
    continent="Europe", region="eastern-europe", stack="vk-yandex",
    year=2025, confidence="medium",
    social=cat(["vk", "instagram"], ["telegram", "youtube"],
               ["datareportal-country-index"],
               "VK remains important; Instagram and Telegram are also used. Measurement is politically sensitive and thinner than for the EU.",
               "VK 仍然重要；Instagram 與 Telegram 也有人用。測量受政治環境影響，薄於歐盟。", 2025),
    messaging=cat(["telegram"], ["whatsapp"],
                  ["similarweb-messaging-2025"],
                  "Similarweb 2025 lists Telegram as number one in Belarus.",
                  "Similarweb 2025 列 Telegram 為白俄羅斯首位。", 2025),
    payments=cat(["cards"], [], ["worldpay-gpr-2026"],
                 "Domestic cards and bank apps; no high-confidence consumer-wallet colour.",
                 "本國卡與銀行 App；不以高信心為消費錢包上色。", 2025),
    search=cat(["google"], ["yandex"], ["statcounter-search"],
               "Google and Yandex both matter; do not assume a Russia-identical Yandex majority without a dated table.",
               "Google 與 Yandex 都重要；沒有註明日期的表格，就不要假定與俄羅斯完全相同的 Yandex 多數。", 2026),
    ai=cat([], [], ["openai-availability-2026", "searchable-ai-2026"],
           "Public comparable AI-share data is thin. No leader is assigned.",
           "可比較的公開 AI 市佔數據薄。不指定領導產品。", 2026),
    notes=N("Tentatively grouped with the VK–Yandex sphere; confidence is medium.",
            "暫歸入 VK／Yandex 圈；信心中等。"),
))

countries.append(eur("MD","MDA","Moldova","摩爾多瓦","eastern-europe",
                     (["telegram"], ["whatsapp"],
                      "Similarweb 2025 lists Telegram as number one in Moldova.",
                      "Similarweb 2025 列 Telegram 為摩爾多瓦首位。"),
                     ["cards"], [],
                     "Card- and bank-app market; thin data.", "卡與銀行 App 市場；數據薄。",
                     confidence="medium"))
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
# ── Africa ────────────────────────────────────────────────────────────────
countries.append(C(
    iso="EG", iso3="EGY", name=N("Egypt", "埃及"),
    continent="Africa", region="northern-africa", stack="whatsapp-meta",
    year=2025, confidence="medium",
    social=cat(["facebook", "youtube", "instagram"], ["tiktok"],
               ["datareportal-country-index"],
               "Facebook remains a central public square in North Africa, with YouTube and Instagram.",
               "在北非，Facebook 仍是核心公開廣場，輔以 YouTube 與 Instagram。", 2025),
    messaging=cat(["whatsapp"], ["messenger", "telegram"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the usual default.",
                  "通常以 WhatsApp 為預設。", 2025),
    payments=cat(["cards"], [], ["worldpay-gpr-2026"],
                 "Cards, cash and local wallets; no single high-confidence rail is assigned.",
                 "卡、現金與本地錢包；不指定單一高信心軌道。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("North African WhatsApp–Meta, Facebook-strong.", "北非 WhatsApp／Meta，Facebook 很強。"),
))
for iso, iso3, en, zh in [("MA","MAR","Morocco","摩洛哥"),("DZ","DZA","Algeria","阿爾及利亞"),
                          ("TN","TUN","Tunisia","突尼西亞"),("LY","LBY","Libya","利比亞")]:
    countries.append(C(
        iso=iso, iso3=iso3, name=N(en, zh),
        continent="Africa", region="northern-africa", stack="whatsapp-meta",
        year=2025, confidence="medium" if iso != "LY" else "low",
        social=cat(["facebook", "instagram", "youtube"], ["tiktok"],
                   ["datareportal-country-index"],
                   "Facebook is still the usual North African public square.",
                   "Facebook 仍是北非常見的公開廣場。", 2025),
        messaging=cat(["whatsapp"], ["messenger"],
                      ["similarweb-messaging-2025"],
                      "WhatsApp is the regional default where measured; Messenger remains widely installed.",
                      "在有測量處，區域預設為 WhatsApp；Messenger 安裝量仍高。", 2025),
        payments=cat(["cards"], [], ["worldpay-gpr-2026"],
                     "No single national rail assigned at high confidence.",
                     "不以高信心指定單一國家軌道。", 2025),
        search=SEARCH_GOOGLE,
        ai=AI_DEFAULT,
        notes=N("North African WhatsApp–Meta / Facebook pattern.", "北非 WhatsApp／Meta／Facebook 格局。"),
    ))

countries.append(C(
    iso="NG", iso3="NGA", name=N("Nigeria", "尼日利亞"),
    continent="Africa", region="western-africa", stack="whatsapp-meta",
    year=2025, confidence="medium",
    social=cat(["facebook", "instagram", "youtube"], ["tiktok", "x"],
               ["datareportal-country-index"],
               "Facebook, Instagram and YouTube are the main public layers; X is notable in news and politics.",
               "Facebook、Instagram、YouTube 是主要公開層；X 在新聞與政治中值得注意。", 2025),
    messaging=cat(["whatsapp"], ["telegram", "messenger"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the default national chat.",
                  "WhatsApp 是全國預設聊天工具。", 2025),
    payments=cat(["nip", "opay"], ["cards"],
                 ["worldpay-gpr-2026", "gsma-sotir-2026"],
                 "Instant bank transfers (NIP) and fintech wallets such as OPay are widely cited; cash and agent networks remain important. Not a single M-Pesa-like monopoly.",
                 "即時銀行轉帳（NIP）與 OPay 等金融科技錢包被廣泛提及；現金與代理網絡仍然重要。不是 M-Pesa 那樣的單一壟斷。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("WhatsApp–Meta with a transfer-and-wallet payments layer (NIP / OPay), not a single mobile-money brand.",
            "WhatsApp／Meta，支付是轉帳加錢包（NIP／OPay），不是單一流動金錢品牌。"),
))

countries.append(C(
    iso="GH", iso3="GHA", name=N("Ghana", "迦納"),
    continent="Africa", region="western-africa", stack="whatsapp-meta",
    year=2025, confidence="medium",
    social=cat(["facebook", "instagram", "youtube"], ["tiktok"],
               ["datareportal-country-index"],
               "Facebook, Instagram and YouTube are the usual public layer.",
               "通常以 Facebook、Instagram、YouTube 為公開層。", 2025),
    messaging=cat(["whatsapp"], ["messenger"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the default.", "WhatsApp 是預設。", 2025),
    payments=cat(["momo-gh"], ["cards"],
                 ["gsma-sotir-2026"],
                 "Mobile money (often branded MoMo in Ghana) is the distinctive everyday rail.",
                 "流動金錢（在迦納常稱為 MoMo）是具特色的日常軌道。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("WhatsApp–Meta with Ghana MoMo as the payment signature.",
            "WhatsApp／Meta，支付簽名是迦納 MoMo。"),
))

for iso, iso3, en, zh in [("SN","SEN","Senegal","塞內加爾"),("CI","CIV","Cote d'Ivoire","科特迪瓦")]:
    countries.append(C(
        iso=iso, iso3=iso3, name=N(en, zh),
        continent="Africa", region="western-africa", stack="whatsapp-meta",
        year=2025, confidence="medium",
        social=cat(["facebook", "instagram"], ["youtube", "tiktok"],
                   ["datareportal-country-index"],
                   "Facebook is the usual public layer in Francophone West Africa.",
                   "在西非法語區，通常以 Facebook 為公開層。", 2025),
        messaging=cat(["whatsapp"], ["messenger"],
                      ["similarweb-messaging-2025"],
                      "WhatsApp is the regional default.", "區域預設為 WhatsApp。", 2025),
        payments=cat(["cards"], [], ["gsma-sotir-2026"],
                     "Mobile money is important across the WAEMU region; this compile does not assign a single brand at high confidence.",
                     "在西非經濟貨幣聯盟區域，流動金錢很重要；本次彙編不以高信心指定單一品牌。", 2025),
        search=SEARCH_GOOGLE,
        ai=AI_DEFAULT,
        notes=N("Francophone West African WhatsApp–Meta, with mobile money in the background.",
                "西非法語區的 WhatsApp／Meta，背景是流動金錢。"),
    ))

countries.append(C(
    iso="KE", iso3="KEN", name=N("Kenya", "肯尼亞"),
    continent="Africa", region="eastern-africa", stack="whatsapp-meta",
    year=2025, confidence="high",
    social=cat(["facebook", "instagram", "youtube"], ["tiktok", "x"],
               ["datareportal-country-index"],
               "Facebook, Instagram and YouTube are the main public layers.",
               "Facebook、Instagram、YouTube 是主要公開層。", 2025),
    messaging=cat(["whatsapp"], ["messenger"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the default chat.",
                  "WhatsApp 是預設聊天工具。", 2025),
    payments=cat(["mpesa"], ["cards"],
                 ["gsma-sotir-2026", "worldpay-gpr-2026"],
                 "M-Pesa is the distinctive everyday payment and money-transfer layer — the original mobile-money signature of East Africa.",
                 "M-Pesa 是具特色的日常支付與匯款層——東非流動金錢的原點簽名。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("WhatsApp–Meta with M-Pesa as one of the world’s clearest payment signatures.",
            "WhatsApp／Meta，M-Pesa 是全球最清楚的支付簽名之一。"),
))

countries.append(C(
    iso="TZ", iso3="TZA", name=N("Tanzania", "坦桑尼亞"),
    continent="Africa", region="eastern-africa", stack="whatsapp-meta",
    year=2025, confidence="high",
    social=cat(["facebook", "instagram", "youtube"], ["tiktok"],
               ["datareportal-country-index"],
               "Facebook, Instagram and YouTube are the usual public layer.",
               "通常以 Facebook、Instagram、YouTube 為公開層。", 2025),
    messaging=cat(["whatsapp"], ["messenger"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the default.", "WhatsApp 是預設。", 2025),
    payments=cat(["mpesa"], ["cards"],
                 ["gsma-sotir-2026", "worldpay-gpr-2026"],
                 "M-Pesa is also the distinctive mobile-money layer in Tanzania.",
                 "在坦桑尼亞，M-Pesa 同樣是具特色的流動金錢層。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("East African WhatsApp–Meta + M-Pesa, like Kenya.",
            "東非 WhatsApp／Meta＋M-Pesa，與肯尼亞相近。"),
))

for iso, iso3, en, zh, conf in [
    ("UG","UGA","Uganda","烏干達","medium"),
    ("RW","RWA","Rwanda","盧旺達","medium"),
]:
    countries.append(C(
        iso=iso, iso3=iso3, name=N(en, zh),
        continent="Africa", region="eastern-africa", stack="whatsapp-meta",
        year=2025, confidence=conf,
        social=cat(["facebook", "youtube"], ["instagram", "tiktok"],
                   ["datareportal-country-index"],
                   "Facebook and YouTube are the usual public layer.",
                   "通常以 Facebook 與 YouTube 為公開層。", 2025),
        messaging=cat(["whatsapp"], ["telegram", "messenger"],
                      ["similarweb-messaging-2025"],
                      "WhatsApp is the regional default; Telegram is also used.",
                      "區域預設為 WhatsApp；Telegram 也有人用。", 2025),
        payments=cat(["mpesa"], [],
                     ["gsma-sotir-2026"],
                     "Mobile money is important across East Africa. M-Pesa and local brands circulate.",
                     "流動金錢在東非很重要。M-Pesa 與本地品牌並存。", 2025),
        search=SEARCH_GOOGLE,
        ai=AI_DEFAULT,
        notes=N("Eastern African WhatsApp–Meta; mobile money is the payments story.",
                "東非 WhatsApp／Meta；支付故事是流動金錢。"),
    ))

countries.append(C(
    iso="ET", iso3="ETH", name=N("Ethiopia", "埃塞俄比亞"),
    continent="Africa", region="eastern-africa", stack="whatsapp-meta",
    year=2025, confidence="medium",
    social=cat(["facebook", "youtube"], ["instagram", "tiktok"],
               ["datareportal-country-index"],
               "Facebook and YouTube are the usual public layer. Ethiopia’s platform mix can be disrupted by connectivity and policy; confidence is moderate.",
               "通常以 Facebook 與 YouTube 為公開層。埃塞俄比亞的平台組合可能因連線與政策而中斷；信心中等。", 2025),
    messaging=cat(["whatsapp"], ["telegram", "messenger"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the regional default; Telegram is also used.",
                  "區域預設為 WhatsApp；Telegram 也有人用。", 2025),
    payments=cat(["cards"], [], ["gsma-sotir-2026"],
                 "Mobile money and bank apps exist; no single brand is assigned at high confidence.",
                 "有流動金錢與銀行 App；不以高信心指定單一品牌。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("Eastern African WhatsApp–Meta; payments left generic because the brand picture is thinner than Kenya.",
            "東非 WhatsApp／Meta；因品牌圖景薄於肯尼亞，支付保持籠統。"),
))

countries.append(C(
    iso="ZA", iso3="ZAF", name=N("South Africa", "南非"),
    continent="Africa", region="southern-africa", stack="whatsapp-meta",
    year=2025, confidence="high",
    social=cat(["facebook", "youtube", "instagram"], ["tiktok", "x"],
               ["datareportal-country-index"],
               "Facebook, YouTube and Instagram are the main public layers.",
               "Facebook、YouTube、Instagram 是主要公開層。", 2025),
    messaging=cat(["whatsapp"], ["messenger"],
                  ["similarweb-messaging-2025"],
                  "WhatsApp is the default national chat.",
                  "WhatsApp 是全國預設聊天工具。", 2025),
    payments=cat(["cards", "payshap"], ["applepay"],
                 ["worldpay-gpr-2026", "gsma-sotir-2026"],
                 "A more card-like market than Kenya, with PayShap as a growing instant-payment rail. Not an M-Pesa-default country.",
                 "比肯尼亞更偏卡，PayShap 是正在成長的即時支付軌道。不是以 M-Pesa 為預設的國家。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("WhatsApp–Meta with a cards + PayShap payments mix, distinct from East African M-Pesa.",
            "WhatsApp／Meta，支付是卡＋PayShap，有別於東非的 M-Pesa。"),
))

for iso, iso3, en, zh, region, conf in [
    ("AO","AGO","Angola","安哥拉","middle-africa","medium"),
    ("CD","COD","Democratic Republic of the Congo","剛果民主共和國","middle-africa","low"),
    ("CM","CMR","Cameroon","喀麥隆","middle-africa","medium"),
    ("ZW","ZWE","Zimbabwe","津巴布韋","southern-africa","medium"),
    ("MZ","MOZ","Mozambique","莫桑比克","southern-africa","medium"),
    ("NA","NAM","Namibia","納米比亞","southern-africa","medium"),
    ("MU","MUS","Mauritius","毛里求斯","eastern-africa","medium"),
]:
    countries.append(C(
        iso=iso, iso3=iso3, name=N(en, zh),
        continent="Africa", region=region, stack="whatsapp-meta",
        year=2025, confidence=conf,
        social=cat(["facebook", "youtube"], ["instagram", "tiktok"],
                   ["datareportal-country-index", "datareportal-2025-global"],
                   "Facebook is the usual public layer. DataReportal warns that commercial messaging figures for much of Sub-Saharan Africa likely under-count real social adoption.",
                   "通常以 Facebook 為公開層。DataReportal 提醒，撒哈拉以南非洲許多商業通訊數字可能低估真實社交使用。", 2025),
        messaging=cat(["whatsapp"], ["messenger"],
                      ["similarweb-messaging-2025", "datareportal-2025-global"],
                      "WhatsApp is the regional default where measured. Official social-adoption figures may under-count messaging apps.",
                      "在有測量處，區域預設為 WhatsApp。官方社交採用數字可能低估通訊 App。", 2025),
        payments=cat(["cards"], [], ["gsma-sotir-2026"],
                     "Mobile money is often important, but a single brand is not assigned at high confidence except where named elsewhere (Kenya, Tanzania, Ghana).",
                     "流動金錢往往重要，但除在其他條目已點名者（肯尼亞、坦桑尼亞、迦納）外，不以高信心指定單一品牌。", 2025),
        search=SEARCH_GOOGLE,
        ai=AI_DEFAULT,
        notes=N("Sub-Saharan WhatsApp–Meta with uneven data; the map should not look more certain than the sources.",
                "撒哈拉以南的 WhatsApp／Meta，數據不均；地圖的確定程度不應高於來源。"),
    ))

# ── Oceania ────────────────────────────────────────────────────────────────
countries.append(C(
    iso="AU", iso3="AUS", name=N("Australia", "澳洲"),
    continent="Oceania", region="australia-nz", stack="anglosphere-mixed",
    year=2025, confidence="high",
    social=cat(["youtube", "instagram", "facebook"], ["tiktok", "x"],
               ["datareportal-country-index", "datareportal-2025-social"],
               "YouTube, Instagram and Facebook are the main public feeds, close to other high-income English-speaking markets.",
               "YouTube、Instagram、Facebook 是主要公開動態，接近其他高收入英語市場。", 2025),
    messaging=cat(["imessage", "whatsapp", "messenger"], [],
                  ["similarweb-messaging-2025"],
                  "MIXED. Similarweb 2025: WhatsApp ranks first on some Android measures, but Messenger leads some daily / monthly active-use measures. iMessage is common on iPhones and missing from Android panels.",
                  "混合。Similarweb 2025：WhatsApp 在部分 Android 指標排第一，但 Messenger 在部分日／月活躍指標領先。iPhone 上 iMessage 很常見，Android 面板看不到。", 2025),
    payments=cat(["cards", "applepay"], ["paypal", "googlepay"],
                 ["worldpay-gpr-2026"],
                 "Cards and contactless wallets (Apple Pay / Google Pay) are everyday. PayPal is strong online. No Pix-like rail.",
                 "卡與感應錢包（Apple Pay／Google Pay）是日常工具。網上 PayPal 很強。沒有類似 Pix 的軌道。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("Anglosphere mixed: iMessage / Messenger / WhatsApp together, cards + Apple Pay, Google, ChatGPT.",
            "英語圈混合：iMessage／Messenger／WhatsApp 並存，卡＋Apple Pay，Google，ChatGPT。"),
))

countries.append(C(
    iso="NZ", iso3="NZL", name=N("New Zealand", "紐西蘭"),
    continent="Oceania", region="australia-nz", stack="anglosphere-mixed",
    year=2025, confidence="high",
    social=cat(["youtube", "facebook", "instagram"], ["tiktok"],
               ["datareportal-country-index"],
               "Close to Australia’s public social mix; Facebook remains very present.",
               "公開社交組合接近澳洲；Facebook 仍然很存在。", 2025),
    messaging=cat(["imessage", "whatsapp", "messenger"], [],
                  ["similarweb-messaging-2025"],
                  "Mixed, like Australia: WhatsApp, Messenger and iMessage together. Android panels under-count iMessage.",
                  "與澳洲一樣屬混合：WhatsApp、Messenger、iMessage 並存。Android 面板低估 iMessage。", 2025),
    payments=cat(["cards", "applepay"], ["paypal"],
                 ["worldpay-gpr-2026"],
                 "Cards and Apple Pay / contactless; no distinctive new rail assigned.",
                 "卡與 Apple Pay／感應支付；不指定新的特色軌道。", 2025),
    search=SEARCH_GOOGLE,
    ai=AI_DEFAULT,
    notes=N("Anglosphere mixed, close to Australia.", "英語圈混合，接近澳洲。"),
))

for iso, iso3, en, zh in [("PG","PNG","Papua New Guinea","巴布亞新幾內亞"),("FJ","FJI","Fiji","斐濟")]:
    countries.append(C(
        iso=iso, iso3=iso3, name=N(en, zh),
        continent="Oceania", region="pacific", stack="whatsapp-meta",
        year=2025, confidence="low",
        social=cat(["facebook"], ["youtube", "instagram"],
                   ["datareportal-country-index"],
                   "Facebook is the usual public internet in Pacific accounts. Data is thin.",
                   "在太平洋地區的描述中，Facebook 通常就是公開互聯網。數據薄。", 2025),
        messaging=cat(["whatsapp", "messenger"], [],
                      ["similarweb-messaging-2025"],
                      "WhatsApp and Messenger are both used; low confidence on which is the default.",
                      "WhatsApp 與 Messenger 都有人用；誰是預設的信心低。", 2025),
        payments=cat(["cards"], [], ["worldpay-gpr-2026"],
                     "Mobile money and cards exist; no high-confidence brand is assigned.",
                     "有流動金錢與卡；不以高信心指定品牌。", 2025),
        search=SEARCH_GOOGLE,
        ai=AI_DEFAULT,
        notes=N("Data-thin Pacific WhatsApp/Facebook markets.", "數據偏薄的太平洋 WhatsApp／Facebook 市場。"),
    ))
# ── Regional defaults for the rest of the map ──────────────────────────────
def infer(stack, social, messaging, payments, search, ai, notes):
    return {
        "stack": stack,
        "social": social,
        "messaging": messaging,
        "payments": payments,
        "search": search,
        "ai": ai,
        "notes": notes,
        "confidence": "low",
        "year": 2025,
    }

regional_defaults = {
    "southeast-asia": infer("whatsapp-meta", ["facebook", "tiktok"], ["whatsapp"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference for smaller Southeast Asian territories not given a full profile: Facebook / WhatsApp / Google, with TikTok often strong. Shown as low confidence.",
          "未獨立建檔的較小東南亞地區，按區域推斷：Facebook／WhatsApp／Google，TikTok 往往很強。以低信心顯示。")),
    "south-asia": infer("whatsapp-meta", ["facebook", "youtube"], ["whatsapp"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference: South Asian WhatsApp–Meta / Facebook / Google pattern. Low confidence.",
          "區域推斷：南亞 WhatsApp／Meta／Facebook／Google 格局。低信心。")),
    "central-asia": infer("whatsapp-meta", ["instagram", "facebook"], ["telegram"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference: Instagram plus Telegram or WhatsApp, Google search, with Yandex as a possible secondary. Low confidence.",
          "區域推斷：Instagram，加上 Telegram 或 WhatsApp，搜尋 Google，Yandex 可能是次選。低信心。")),
    "western-asia": infer("whatsapp-meta", ["instagram", "facebook"], ["whatsapp"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference: WhatsApp + Instagram/Facebook + cards + Google. Low confidence.",
          "區域推斷：WhatsApp＋Instagram／Facebook＋卡＋Google。低信心。")),
    "western-europe": infer("whatsapp-meta", ["instagram", "facebook"], ["whatsapp"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference for microstates: WhatsApp, Instagram/Facebook, cards, Google, ChatGPT. Low confidence.",
          "微型國家的區域推斷：WhatsApp、Instagram／Facebook、卡、Google、ChatGPT。低信心。")),
    "northern-europe": infer("whatsapp-meta", ["instagram", "facebook"], ["whatsapp"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference: Nordic/Baltic open-web pattern. Low confidence for unlisted territories.",
          "區域推斷：北歐／波羅的海開放網絡格局。未列地區為低信心。")),
    "southern-europe": infer("whatsapp-meta", ["instagram", "facebook"], ["whatsapp"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference: Southern European WhatsApp–Meta, cards, Google. Low confidence.",
          "區域推斷：南歐 WhatsApp／Meta、卡、Google。低信心。")),
    "eastern-europe": infer("whatsapp-meta", ["facebook", "instagram"], ["whatsapp"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference for smaller Eastern European states: WhatsApp/Facebook, cards, Google — unless they sit closer to the VK–Yandex or Telegram pattern (see Russia, Belarus, Moldova, Ukraine).",
          "較小東歐國家的區域推斷：WhatsApp／Facebook、卡、Google——除非更接近 VK／Yandex 或 Telegram 格局（見俄、白、摩、烏）。")),
    "northern-america": infer("anglosphere-mixed", ["facebook", "instagram"], ["imessage", "whatsapp"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference for unlisted North American territories: mixed messaging, cards, Google. Low confidence.",
          "未列北美地區的區域推斷：混合通訊、卡、Google。低信心。")),
    "central-america": infer("whatsapp-meta", ["facebook", "instagram"], ["whatsapp"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference: Central American WhatsApp–Meta. Low confidence.",
          "區域推斷：中美 WhatsApp／Meta。低信心。")),
    "caribbean": infer("whatsapp-meta", ["facebook", "instagram"], ["whatsapp"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference: Caribbean WhatsApp / Facebook. Low confidence. A few markets may skew to Snapchat on some Android rankings.",
          "區域推斷：加勒比 WhatsApp／Facebook。低信心。部分市場在某些 Android 排名中可能偏 Snapchat。")),
    "south-america": infer("whatsapp-meta", ["instagram", "facebook"], ["whatsapp"], ["mercadopago", "cards"], ["google"], ["chatgpt"],
        N("Regional inference: Spanish-speaking South American WhatsApp–Meta, Mercado Pago / cards, Google. Pix is not assumed outside Brazil.",
          "區域推斷：西班牙語南美 WhatsApp／Meta、Mercado Pago／卡、Google。不假定巴西以外已是 Pix。")),
    "northern-africa": infer("whatsapp-meta", ["facebook"], ["whatsapp"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference: North African Facebook / WhatsApp / Google. Low confidence.",
          "區域推斷：北非 Facebook／WhatsApp／Google。低信心。")),
    "western-africa": infer("whatsapp-meta", ["facebook"], ["whatsapp"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference: West African WhatsApp–Meta; mobile money is often important but brands vary. DataReportal warns that messaging use may be under-counted. Low confidence.",
          "區域推斷：西非 WhatsApp／Meta；流動金錢往往重要但品牌各異。DataReportal 提醒通訊使用可能被低估。低信心。")),
    "eastern-africa": infer("whatsapp-meta", ["facebook"], ["whatsapp"], ["mpesa"], ["google"], ["chatgpt"],
        N("Regional inference: East African WhatsApp–Meta; M-Pesa-like mobile money is common but not universal. Low confidence outside Kenya and Tanzania.",
          "區域推斷：東非 WhatsApp／Meta；類似 M-Pesa 的流動金錢常見但並非處處皆是。肯尼亞與坦桑尼亞以外為低信心。")),
    "middle-africa": infer("whatsapp-meta", ["facebook"], ["whatsapp"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference and often data-poor: Facebook / WhatsApp / Google. Show the caveat prominently.",
          "區域推斷且往往資料不足：Facebook／WhatsApp／Google。必須明顯標示保留。")),
    "southern-africa": infer("whatsapp-meta", ["facebook"], ["whatsapp"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference: WhatsApp–Meta, cards or mobile money, Google. Low confidence outside South Africa.",
          "區域推斷：WhatsApp／Meta，卡或流動金錢，Google。南非以外為低信心。")),
    "pacific": infer("whatsapp-meta", ["facebook"], ["whatsapp", "messenger"], ["cards"], ["google"], ["chatgpt"],
        N("Regional inference for Pacific islands: Facebook is often the public internet; WhatsApp and Messenger are both used. Low confidence.",
          "太平洋島嶼的區域推斷：Facebook 往往就是公開互聯網；WhatsApp 與 Messenger 都有人用。低信心。")),
}

# Validate
from collections import Counter

isos = [c["iso"] for c in countries]
dups = [x for x in isos if isos.count(x) > 1]
if dups:
    raise SystemExit(f"duplicate iso {sorted(set(dups))}")
iso3s = [c["iso3"] for c in countries]
if "IDA" in iso3s:
    raise SystemExit("bad iso3 IDA")
assert countries[isos.index("ID")]["iso3"] == "IDN"

platforms = json.loads((ROOT / "platforms.json").read_text())["platforms"]
stacks = json.loads((ROOT / "platforms.json").read_text())["stacks"]
sources = json.loads((ROOT / "sources.json").read_text())["sources"]
regions = json.loads((ROOT / "regions.json").read_text())["regions"]

missing_p = set()
missing_s = set()
for c in countries:
    if c["region"] not in regions:
        raise SystemExit(f"bad region {c['iso']} {c['region']}")
    if c["stack"] not in stacks:
        raise SystemExit(f"bad stack {c['iso']} {c['stack']}")
    for dim in ("social", "messaging", "payments", "search", "ai"):
        for pid in c[dim]["dominant"] + c[dim]["secondary"]:
            if pid not in platforms:
                missing_p.add((c["iso"], dim, pid))
        for sid in c[dim]["sources"]:
            if sid not in sources:
                missing_s.add((c["iso"], dim, sid))

if missing_p or missing_s:
    raise SystemExit(f"missing platforms {missing_p} sources {missing_s}")

payload = {
    "compiled": "2026-11-22",
    "timezone": "Asia/Shanghai",
    "description": "Qualitative, cited country profiles of internet life circles. No invented percentages.",
    "count": len(countries),
    "countries": countries,
}
defaults_out = {
    "compiled": "2026-11-22",
    "description": "Low-confidence regional inference for map countries without a full profile. The UI must label these as data-poor / inferred.",
    "defaults": regional_defaults,
}

(ROOT / "countries.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
(ROOT / "regional-defaults.json").write_text(json.dumps(defaults_out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("countries", len(countries))
print("confidence", dict(Counter(c["confidence"] for c in countries)))
print("stacks", dict(Counter(c["stack"] for c in countries)))
print("regions_used", len(Counter(c["region"] for c in countries)))
