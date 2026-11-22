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
