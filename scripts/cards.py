"""Builds the station cards in assets/cards/. Run: python scripts/cards.py

Every card shares one frame (station tag, title, description, stack, link) and
carries its own small animated vignette. Motion is transform/opacity only.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "cards"
OUT.mkdir(parents=True, exist_ok=True)

PAPER, SURFACE, INK, MUTED, ACCENT, RULE = "#F4F1EA", "#EAE5DA", "#14161A", "#5F6168", "#2F55E4", "#CFC8B8"

BASE_STYLE = f"""
    .d{{font-family:'Segoe UI Variable Display','Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif}}
    .m{{font-family:ui-monospace,SFMono-Regular,'Cascadia Mono',Consolas,Menlo,monospace}}
    .ta{{font-family:'Nirmala UI','Tamil Sangam MN','Noto Sans Tamil',Latha,sans-serif}}
    .ink{{fill:{INK}}}.mut{{fill:{MUTED}}}.acc{{fill:{ACCENT}}}
    @keyframes up{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
    @keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
    @keyframes nudge{{0%,100%{{transform:none}}50%{{transform:translateX(6px)}}}}
    .e{{animation:up .7s cubic-bezier(.2,.8,.2,1) both}}
    .e1{{animation-delay:.05s}}.e2{{animation-delay:.13s}}.e3{{animation-delay:.21s}}.e4{{animation-delay:.29s}}.e5{{animation-delay:.37s}}
    .v{{animation:fade .8s ease-out .3s both}}
    .arrow{{animation:nudge 1.8s ease-in-out infinite}}
"""

REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}.alt{opacity:0}}"


def svg(w, h, title, desc, style, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">
  <title id="t">{title}</title>
  <desc id="d">{desc}</desc>
  <style>{BASE_STYLE}{style}
    {REDUCED}
  </style>
  <rect width="{w}" height="{h}" rx="24" fill="{PAPER}"/>
{body}
</svg>
"""


def half(name, station, title, desc_lines, stack_lines, vignette, style, desc_alt):
    desc = "".join(
        f'<text x="40" y="{150 + i * 24}" class="d ink" font-size="16">{line}</text>' for i, line in enumerate(desc_lines)
    )
    stack = "".join(
        f'<text x="40" y="{244 + i * 20}" class="m mut" font-size="12" letter-spacing=".4">{line}</text>'
        for i, line in enumerate(stack_lines)
    )
    body = f"""  <g class="e e1">
    <circle cx="47" cy="47" r="7" fill="{PAPER}" stroke="{INK}" stroke-width="3.5"/>
    <text x="64" y="51.5" class="m mut" font-size="12" letter-spacing="1.3">{station}</text>
  </g>
  <text x="38" y="106" class="d ink e e2" font-size="34" font-weight="700" letter-spacing="-.8">{title}</text>
  <g class="e e3">{desc}</g>
  <g class="e e4">{stack}</g>
  <g class="e e5">
    <text x="40" y="320" class="d ink" font-size="15" font-weight="600">View repository</text>
    <g class="arrow"><text x="160" y="320" class="d acc" font-size="16" font-weight="700">→</text></g>
  </g>
  <g class="v">
{vignette}
  </g>"""
    (OUT / f"{name}.svg").write_text(svg(600, 360, title, desc_alt, style, body), encoding="utf-8")


# ---------------------------------------------------------------- 01 shop
receipt_style = """
    @keyframes print{0%{transform:translateY(-236px);opacity:1}40%,86%{transform:none;opacity:1}100%{transform:none;opacity:0}}
    @keyframes third{0%,33.3%{opacity:1}33.4%,100%{opacity:0}}
    .rc{animation:print 6s cubic-bezier(.45,0,.2,1) infinite}
    .n{animation:third 18s linear infinite}.n2{animation-delay:-12s}.n3{animation-delay:-6s}
"""
zig = "l-11 8 l-11 -8 " * 6
bars, bx = "", 418
for bw in [2, 1, 3, 1, 2, 1, 1, 3, 2, 1, 2, 3, 1, 2, 1, 3, 1, 2, 2, 1, 3, 1, 2]:
    bars += f'<rect x="{bx}" y="266" width="{bw}" height="18" fill="{INK}"/>'
    bx += bw + 2.4
receipt = f"""    <defs><clipPath id="slot"><rect x="380" y="84" width="180" height="250"/></clipPath></defs>
    <rect x="384" y="68" width="172" height="20" rx="10" fill="{INK}"/>
    <g clip-path="url(#slot)"><g class="rc">
      <path d="M404 78 H536 V300 {zig}Z" fill="#FFFFFF"/>
      <text x="418" y="108" class="m ink n" font-size="11" font-weight="700">BILL-000001</text>
      <text x="418" y="108" class="m ink n n2 alt" font-size="11" font-weight="700">BILL-000002</text>
      <text x="418" y="108" class="m ink n n3 alt" font-size="11" font-weight="700">BILL-000003</text>
      <text x="418" y="124" class="m mut" font-size="8.5" letter-spacing=".6">SHREE ANNAPURNA</text>
      <rect x="418" y="144" width="62" height="6" rx="3" fill="{RULE}"/><rect x="498" y="144" width="24" height="6" rx="3" fill="{RULE}"/>
      <rect x="418" y="164" width="76" height="6" rx="3" fill="{RULE}"/><rect x="498" y="164" width="24" height="6" rx="3" fill="{RULE}"/>
      <rect x="418" y="184" width="50" height="6" rx="3" fill="{RULE}"/><rect x="498" y="184" width="24" height="6" rx="3" fill="{RULE}"/>
      <text x="418" y="222" class="m ink" font-size="10" font-weight="700">TOTAL</text>
      <rect x="488" y="214" width="34" height="9" rx="3" fill="{ACCENT}"/>
      <text x="418" y="248" class="m ink n" font-size="10">PAID · CASH</text>
      <text x="418" y="248" class="m ink n n2 alt" font-size="10">PAID · UPI</text>
      <text x="418" y="248" class="m ink n n3 alt" font-size="10">PAID · CARD</text>
      {bars}
    </g></g>"""
half(
    "smart-billing", "STATION 01 · SHOP COUNTER", "Smart Billing",
    ["Billing and inventory for Shree", "Annapurna Edible Oil Company. Each", "sale and its stock change commit together."],
    ["JAVA 17 · SWING + FLATLAF", "MYSQL · MAVEN"],
    receipt, receipt_style,
    "Java Swing billing and inventory system for Shree Annapurna Edible Oil Company, with atomic invoices and stock deduction.",
)

# ---------------------------------------------------------------- 02 classroom
orbit_style = """
    @keyframes spin{to{transform:rotate(360deg)}}
    .o{transform-origin:470px 186px;animation:spin linear infinite}
    .o1{animation-duration:7s}.o2{animation-duration:13s;animation-delay:-5s}.o3{animation-duration:24s;animation-delay:-15s}
"""
orbits = f"""    <g fill="none" stroke="{RULE}" stroke-width="1.6" stroke-dasharray="3 6">
      <circle cx="470" cy="186" r="48"/><circle cx="470" cy="186" r="80"/><circle cx="470" cy="186" r="112"/>
    </g>
    <circle cx="470" cy="186" r="20" fill="{INK}"/>
    <g class="o o1"><circle cx="518" cy="186" r="7" fill="{PAPER}" stroke="{INK}" stroke-width="3"/></g>
    <g class="o o2"><circle cx="550" cy="186" r="10" fill="{ACCENT}"/><circle cx="566" cy="186" r="3" fill="{INK}"/></g>
    <g class="o o3"><circle cx="582" cy="186" r="8" fill="{PAPER}" stroke="{INK}" stroke-width="3"/><ellipse cx="582" cy="186" rx="15" ry="4.5" fill="none" stroke="{INK}" stroke-width="2.4"/></g>
    <rect x="420" y="308" width="100" height="24" rx="12" fill="{INK}"/>
    <text x="470" y="324" text-anchor="middle" class="m" fill="{PAPER}" font-size="10.5" font-weight="700" letter-spacing="1.2">ENTER VR</text>"""
half(
    "spacexr", "STATION 02 · CLASSROOM", "SpaceXR",
    ["The Solar System in a browser tab.", "Click a planet, read its story, take", "the quiz, step into VR where it works."],
    ["A-FRAME · WEBXR · VANILLA JS", "NO BUILD STEP · NO BACKEND"],
    orbits, orbit_style,
    "Browser-based interactive Solar System with planet info panels, a quiz and a WebXR VR entry point.",
)

# ---------------------------------------------------------------- 03 field
leaf_style = """
    @keyframes scan{0%{transform:translateY(88px);opacity:1}70%{transform:translateY(296px);opacity:1}74%,100%{transform:translateY(296px);opacity:0}}
    @keyframes hit{0%{opacity:0;transform:scale(.4)}6%,45%{opacity:1;transform:none}60%,100%{opacity:0;transform:none}}
    .scan{animation:scan 3.4s cubic-bezier(.5,0,.5,1) infinite}
    .hit{transform-box:fill-box;transform-origin:center;animation:hit 3.4s ease-out infinite}
"""
leaf_d = "M470 92 C548 124 560 228 470 292 C380 228 392 124 470 92 Z"
leaf = f"""    <defs><clipPath id="leaf"><path d="{leaf_d}"/></clipPath></defs>
    <g fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round">
      <path d="M390 98 V80 H408"/><path d="M532 80 H550 V98"/><path d="M390 286 V304 H408"/><path d="M532 304 H550 V286"/>
    </g>
    <path d="{leaf_d}" fill="#DCE5D2"/>
    <g stroke="{INK}" stroke-linecap="round" fill="none">
      <path d="M470 104 V284" stroke-width="2"/>
      <g stroke-width="1.6" opacity=".55"><path d="M470 150 L505 128"/><path d="M470 150 L435 128"/><path d="M470 198 L515 170"/><path d="M470 198 L425 170"/><path d="M470 244 L503 222"/><path d="M470 244 L437 222"/></g>
    </g>
    <circle cx="500" cy="180" r="6" fill="#8A6A33"/><circle cx="447" cy="214" r="5" fill="#8A6A33"/><circle cx="492" cy="238" r="4" fill="#8A6A33"/>
    <g clip-path="url(#leaf)"><g class="scan"><rect x="380" y="-16" width="180" height="16" fill="{ACCENT}" opacity=".14"/><rect x="380" y="-2" width="180" height="3" fill="{ACCENT}"/></g></g>
    <path d="{leaf_d}" fill="none" stroke="{INK}" stroke-width="3"/>
    <g fill="none" stroke="{ACCENT}" stroke-width="2.5">
      <circle cx="500" cy="180" r="13" class="hit" style="animation-delay:1.08s"/>
      <circle cx="447" cy="214" r="12" class="hit" style="animation-delay:1.4s"/>
      <circle cx="492" cy="238" r="11" class="hit" style="animation-delay:1.62s"/>
    </g>
    <text x="470" y="334" text-anchor="middle" class="m mut" font-size="10.5" letter-spacing="1.2">PHOTO → DIAGNOSIS</text>"""
half(
    "farmsense-ai", "STATION 03 · FIELD", "FarmSense AI",
    ["Photograph a sick crop, get a", "diagnosis, then irrigation, rotation", "and yield plans for a small farm."],
    ["GEMINI VISION · VERCEL FUNCTIONS", "HTML · CSS · JAVASCRIPT"],
    leaf, leaf_style,
    "Farm assistant that diagnoses crop disease from a photo and plans irrigation, crop rotation and yield.",
)

# ---------------------------------------------------------------- 04 sky
sky_style = """
    @keyframes drop{0%{transform:translateY(0);opacity:0}15%{opacity:1}100%{transform:translateY(54px);opacity:0}}
    @keyframes tier{0%,21%{transform:none}25%,46%{transform:translateX(48px)}50%,71%{transform:translateX(96px)}75%,96%{transform:translateX(144px)}100%{transform:none}}
    .r{animation:drop 1.1s linear infinite}
    .tier{animation:tier 8s cubic-bezier(.6,0,.2,1) infinite}
"""
drops = "".join(
    f'<path d="M{x} 180 v14" class="r" style="animation-delay:-{dly}s"/>'
    for x, dly in [(430, .1), (451, .62), (472, .33), (493, .85), (514, .5)]
)
segs = "".join(
    f'<rect x="{382 + i * 48}" y="262" width="44" height="14" rx="3" fill="{INK}" opacity="{op}"/>'
    f'<text x="{404 + i * 48}" y="296" text-anchor="middle" class="m mut" font-size="9.5" letter-spacing=".6">{lab}</text>'
    for i, (op, lab) in enumerate([(.14, "LOW"), (.32, "MOD"), (.58, "HIGH"), (.9, "SEVERE")])
)
sky = f"""    <path d="M414 166 H526 C548 166 556 136 536 124 C536 96 504 84 486 98 C474 72 430 76 428 108 C404 110 394 166 414 166 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>
    <g stroke="{ACCENT}" stroke-width="3" stroke-linecap="round">{drops}</g>
    <text x="382" y="252" class="m mut" font-size="10" letter-spacing="1.1">TOMORROW · RISK</text>
    {segs}
    <rect x="378" y="258" width="52" height="22" rx="6" fill="none" stroke="{ACCENT}" stroke-width="3" class="tier"/>
    <text x="470" y="334" text-anchor="middle" class="m mut" font-size="10.5" letter-spacing="1.2">PREDICT_PROBA → ADVISORY</text>"""
half(
    "weatherguard-ai", "STATION 04 · SKY", "WeatherGuard AI",
    ["Live weather in, tomorrow's rain", "probability out, then a plain advisory", "from LOW to SEVERE."],
    ["PYTHON · FLASK · SCIKIT-LEARN", "RANDOM FOREST · OPENWEATHERMAP"],
    sky, sky_style,
    "Weather risk prediction: live OpenWeatherMap data, a Random Forest RainTomorrow model and a four-tier advisory.",
)

# ---------------------------------------------------------------- 05 browser
browser_style = """
    @keyframes half{0%,49.9%{opacity:1}50%,100%{opacity:0}}
    @keyframes badge{0%,21%{opacity:0;transform:translateY(6px)}25%,46%{opacity:1;transform:none}50%,100%{opacity:0}}
    @keyframes sweep{0%{transform:translateY(140px);opacity:1}20%{transform:translateY(288px);opacity:1}21%,100%{transform:translateY(288px);opacity:0}}
    .ua{animation:half 10s linear infinite}.ub{animation-delay:-5s}
    .ba{animation:badge 10s ease-out infinite}.bb{animation-delay:-5s}
    .sw{animation:sweep 5s cubic-bezier(.5,0,.5,1) infinite}
"""
browser = f"""    <defs><clipPath id="page"><rect x="380" y="138" width="180" height="150"/></clipPath></defs>
    <rect x="378" y="76" width="184" height="214" rx="14" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>
    <circle cx="396" cy="94" r="3.5" fill="{RULE}"/><circle cx="408" cy="94" r="3.5" fill="{RULE}"/><circle cx="420" cy="94" r="3.5" fill="{RULE}"/>
    <rect x="390" y="106" width="160" height="22" rx="11" fill="{SURFACE}"/>
    <text x="402" y="121" class="m ink ua" font-size="9.5">paypa1-verify.xyz/login</text>
    <text x="402" y="121" class="m ink ua ub alt" font-size="9.5">github.com/login</text>
    <rect x="396" y="150" width="118" height="8" rx="4" fill="{SURFACE}"/>
    <rect x="396" y="166" width="146" height="8" rx="4" fill="{SURFACE}"/>
    <rect x="396" y="182" width="92" height="8" rx="4" fill="{SURFACE}"/>
    <rect x="396" y="202" width="62" height="18" rx="9" fill="{SURFACE}"/>
    <g clip-path="url(#page)"><g class="sw"><rect x="380" y="-18" width="180" height="18" fill="{ACCENT}" opacity=".14"/><rect x="380" y="-2" width="180" height="3" fill="{ACCENT}"/></g></g>
    <g class="ba"><rect x="398" y="234" width="144" height="36" rx="10" fill="{INK}"/><text x="470" y="256" text-anchor="middle" class="m" fill="{PAPER}" font-size="10.5" font-weight="700" letter-spacing=".8">BLOCKED · PHISHING</text></g>
    <g class="ba bb alt"><rect x="398" y="234" width="144" height="36" rx="10" fill="none" stroke="{INK}" stroke-width="2.5"/><text x="470" y="256" text-anchor="middle" class="m ink" font-size="10.5" font-weight="700" letter-spacing=".8">TRUSTED DOMAIN</text></g>
    <text x="470" y="334" text-anchor="middle" class="m mut" font-size="10.5" letter-spacing="1.2">18 URL FEATURES → XGBOOST</text>"""
half(
    "phishsentinel", "STATION 05 · BROWSER", "PhishSentinel",
    ["A Chrome extension that checks every", "page you open against an XGBoost URL", "model and brand-protection rules."],
    ["XGBOOST · FASTAPI", "CHROME MV3 · REACT + VITE"],
    browser, browser_style,
    "Phishing URL detection: an 18-feature XGBoost model behind FastAPI, a security rule layer, and a Chrome extension.",
)

# ---------------------------------------------------------------- 06 phone
chat_style = """
    @keyframes b1{0%,3%{opacity:0;transform:translateY(10px)}8%,88%{opacity:1;transform:none}95%,100%{opacity:0}}
    @keyframes b2{0%,20%{opacity:0;transform:translateY(10px)}25%,88%{opacity:1;transform:none}95%,100%{opacity:0}}
    @keyframes b3{0%,37%{opacity:0;transform:translateY(10px)}42%,88%{opacity:1;transform:none}95%,100%{opacity:0}}
    @keyframes blink{0%,100%{opacity:1}50%{opacity:.25}}
    .b1{animation:b1 9s ease-out infinite}.b2{animation:b2 9s ease-out infinite}.b3{animation:b3 9s ease-out infinite}
    .live{animation:blink 1.6s ease-in-out infinite}
"""
chat = f"""    <rect x="396" y="54" width="148" height="276" rx="26" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>
    <rect x="446" y="64" width="48" height="6" rx="3" fill="{INK}"/>
    <circle cx="416" cy="92" r="4" class="acc live"/>
    <text x="426" y="96" class="d ink" font-size="11.5" font-weight="700">JanKavach</text>
    <g class="b1"><rect x="410" y="110" width="112" height="44" rx="12" fill="{SURFACE}"/>
      <text x="420" y="128" class="d ink" font-size="10.5">Your KYC expires</text><text x="420" y="143" class="d ink" font-size="10.5">today. Send OTP.</text></g>
    <g class="b2"><rect x="418" y="166" width="112" height="44" rx="12" fill="{INK}"/>
      <text x="428" y="184" class="d" fill="{PAPER}" font-size="10.5" font-weight="600">Likely a scam.</text><text x="428" y="199" class="d" fill="{PAPER}" font-size="10.5">Never share OTPs.</text></g>
    <g class="b3"><rect x="418" y="222" width="112" height="44" rx="12" fill="{ACCENT}"/>
      <text x="428" y="240" class="d" fill="#FFFFFF" font-size="10.5" font-weight="600">Lost money?</text><text x="428" y="255" class="d" fill="#FFFFFF" font-size="10.5">Call 1930 now.</text></g>
    <rect x="410" y="292" width="120" height="22" rx="11" fill="{SURFACE}"/>"""
half(
    "jankavach", "STATION 06 · PHONE", "JanKavach",
    ["Forward a suspicious text or voice", "note to a Telegram bot. Get a verdict,", "and the 1930 helpline if money is gone."],
    ["PYTHON · GEMINI · TELEGRAM BOT API", "STREAMLIT · SQLITE"],
    chat, chat_style,
    "Telegram bot and dashboard that analyses suspicious texts and voice notes for fraud and routes victims to the 1930 helpline.",
)

# ---------------------------------------------------------------- 07 home (wide)
ff_style = """
    @keyframes rA1{0%,2%{opacity:0;transform:translateY(-8px)}6%,44%{opacity:1;transform:none}48%,100%{opacity:0}}
    @keyframes rB1{0%,26%{opacity:0;transform:translateY(-8px)}30%,44%{opacity:1;transform:none}48%,100%{opacity:0}}
    @keyframes rB2{0%,52%{opacity:0;transform:translateY(-8px)}56%,94%{opacity:1;transform:none}98%,100%{opacity:0}}
    @keyframes rA2{0%,76%{opacity:0;transform:translateY(-8px)}80%,94%{opacity:1;transform:none}98%,100%{opacity:0}}
    @keyframes pAB{0%,8%{opacity:0;transform:none}10%{opacity:1;transform:none}26%{opacity:1;transform:translateX(92px)}28%,100%{opacity:0;transform:translateX(92px)}}
    @keyframes pBA{0%,58%{opacity:0;transform:translateX(92px)}60%{opacity:1;transform:translateX(92px)}76%{opacity:1;transform:none}78%,100%{opacity:0;transform:none}}
    .rA1{animation:rA1 12s ease-out infinite}.rB1{animation:rB1 12s ease-out infinite}
    .rB2{animation:rB2 12s ease-out infinite}.rA2{animation:rA2 12s ease-out infinite}
    .pAB{animation:pAB 12s cubic-bezier(.5,0,.5,1) infinite}.pBA{animation:pBA 12s cubic-bezier(.5,0,.5,1) infinite}
    .hide{opacity:0}
"""


def phone(x, header, header_cls, cls_new):
    rows = "".join(
        f'<circle cx="{x + 22}" cy="{140 + i * 26}" r="6" fill="{SURFACE}"/>'
        f'<rect x="{x + 34}" y="{137 + i * 26}" width="{[46, 38, 52, 32][i]}" height="6" rx="3" fill="{RULE}"/>'
        f'<text x="{x + 88}" y="{143 + i * 26}" class="m mut" font-size="9">₹</text>'
        f'<rect x="{x + 96}" y="{137 + i * 26}" width="16" height="6" rx="3" fill="{RULE}"/>'
        for i in range(4)
    )
    new = "".join(
        f'<g class="{c} hide"><rect x="{x + 10}" y="104" width="108" height="22" rx="8" fill="{ACCENT}" opacity=".14"/>'
        f'<circle cx="{x + 22}" cy="115" r="6" fill="{ACCENT}"/><rect x="{x + 34}" y="112" width="40" height="6" rx="3" fill="{ACCENT}"/>'
        f'<text x="{x + 88}" y="118" class="m acc" font-size="9" font-weight="700">₹</text><rect x="{x + 96}" y="112" width="16" height="6" rx="3" fill="{ACCENT}"/></g>'
        for c in cls_new
    )
    return f"""    <rect x="{x}" y="50" width="128" height="250" rx="22" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>
    <rect x="{x + 44}" y="59" width="40" height="5" rx="2.5" fill="{INK}"/>
    <text x="{x + 64}" y="90" text-anchor="middle" class="{header_cls} ink" font-size="11.5" font-weight="700">{header}</text>
    {new}
    {rows}
    <rect x="{x + 10}" y="242" width="108" height="44" rx="10" fill="{INK}"/>
    <text x="{x + 22}" y="260" class="m" fill="{PAPER}" opacity=".7" font-size="8.5" letter-spacing="1">BALANCE</text>
    <rect x="{x + 22}" y="268" width="58" height="7" rx="3" fill="{PAPER}"/>"""


ff_vignette = f"""{phone(790, "வரவு · செலவு", "ta", ["rA1", "rA2"])}
{phone(1010, "Income · Expense", "d", ["rB1", "rB2"])}
    <path d="M926 175 H1002" stroke="{RULE}" stroke-width="2" stroke-dasharray="3 6" stroke-linecap="round"/>
    <g class="pAB hide"><rect x="912" y="167" width="24" height="16" rx="5" fill="{ACCENT}"/><text x="924" y="179" text-anchor="middle" class="m" fill="#FFFFFF" font-size="10" font-weight="700">₹</text></g>
    <g class="pBA hide"><rect x="912" y="167" width="24" height="16" rx="5" fill="{ACCENT}"/><text x="924" y="179" text-anchor="middle" class="m" fill="#FFFFFF" font-size="10" font-weight="700">₹</text></g>
    <text x="854" y="326" text-anchor="middle" class="m mut" font-size="10.5" letter-spacing="1.2">PHONE A · TAMIL</text>
    <text x="1074" y="326" text-anchor="middle" class="m mut" font-size="10.5" letter-spacing="1.2">PHONE B · ENGLISH</text>"""

def wide(name, title, tag, marker, quote_lines, desc_lines, stack, numbers, vignette, style, desc_alt):
    stats = "".join(
        f'<text x="{44 + i * 150}" y="326" class="d ink" font-size="38" font-weight="700" letter-spacing="-1">{n}</text>'
        f'<text x="{46 + i * 150}" y="350" class="m mut" font-size="11" letter-spacing="1.2">{lab}</text>'
        for i, (n, lab) in enumerate(numbers)
    )
    quote = "".join(
        f'<text x="42" y="{160 + i * 28}" class="d ink" font-size="21">{line}</text>' for i, line in enumerate(quote_lines)
    )
    desc = "".join(
        f'<text x="42" y="{220 + i * 22}" class="d mut" font-size="15.5">{line}</text>' for i, line in enumerate(desc_lines)
    )
    body = f"""  <g class="e e1">
    <circle cx="51" cy="49" r="10" fill="{PAPER}" stroke="{marker[0]}" stroke-width="{marker[1]}"/>
    <text x="72" y="53.5" class="m mut" font-size="12" letter-spacing="1.3">{tag}</text>
  </g>
  <text x="40" y="118" class="d ink e e2" font-size="48" font-weight="700" letter-spacing="-1.4">{title}</text>
  <g class="e e3">{quote}</g>
  <g class="e e4">
    {desc}
    <text x="42" y="270" class="m mut" font-size="12" letter-spacing=".4">{stack}</text>
  </g>
  <g class="e e5">{stats}</g>
  <g class="e e5">
    <text x="560" y="350" class="d ink" font-size="15" font-weight="600">View repository</text>
    <g class="arrow"><text x="680" y="350" class="d acc" font-size="16" font-weight="700">→</text></g>
  </g>
  <g class="v">
{vignette}
  </g>"""
    (OUT / f"{name}.svg").write_text(svg(1200, 380, title, desc_alt, style, body), encoding="utf-8")


wide(
    "family-finance", "Family Finance", "STATION 07 · HOME", (INK, 4.5),
    ["Two people, two phones, one shared set of books,", "kept to the paisa."],
    ["Offline-first Android money manager in Tamil and English. Either phone",
     "can add or edit, and both stay in sync after a day offline in the fields."],
    "KOTLIN · JETPACK COMPOSE · MATERIAL 3 · FIREBASE AUTH + FIRESTORE",
    [("195", "UNIT TESTS"), ("29", "RULES TESTS"), ("22", "DEVICE TESTS")],
    ff_vignette, ff_style,
    "Private, offline-first family money manager for Android in Tamil and English, with 195 unit tests, 29 rules tests and 22 device tests.",
)

# ---------------------------------------------------------------- 08 git history (wide)
dig_style = """
    @keyframes slip{0%,8%{transform:none}14%,90%{transform:translateY(16px)}98%,100%{transform:none}}
    @keyframes was{0%,10%{opacity:1}13%,90%{opacity:0}97%,100%{opacity:1}}
    @keyframes now{0%,10%{opacity:0}13%,90%{opacity:1}97%,100%{opacity:0}}
    @keyframes bore1{0%,16%{transform:scaleY(0);opacity:1}30%,90%{transform:none;opacity:1}96%,100%{transform:none;opacity:0}}
    @keyframes bore2{0%,30%{transform:scaleY(0);opacity:1}44%,90%{transform:none;opacity:1}96%,100%{transform:none;opacity:0}}
    @keyframes bore3{0%,44%{transform:scaleY(0);opacity:1}58%,90%{transform:none;opacity:1}96%,100%{transform:none;opacity:0}}
    @keyframes tag1{0%,29%{opacity:0;transform:translateY(6px)}33%,90%{opacity:1;transform:none}96%,100%{opacity:0}}
    @keyframes tag2{0%,43%{opacity:0;transform:translateY(6px)}47%,90%{opacity:1;transform:none}96%,100%{opacity:0}}
    @keyframes tag3{0%,57%{opacity:0;transform:translateY(6px)}61%,90%{opacity:1;transform:none}96%,100%{opacity:0}}
    .slip{animation:slip 10s cubic-bezier(.6,0,.2,1) infinite}
    .was{animation:was 10s linear infinite}.now{animation:now 10s linear infinite}
    .bore{transform-box:fill-box;transform-origin:top}
    .b1{animation:bore1 10s cubic-bezier(.5,0,.3,1) infinite}.b2{animation:bore2 10s cubic-bezier(.5,0,.3,1) infinite}.b3{animation:bore3 10s cubic-bezier(.5,0,.3,1) infinite}
    .t1{animation:tag1 10s ease-out infinite}.t2{animation:tag2 10s ease-out infinite}.t3{animation:tag3 10s ease-out infinite}
"""


def rock(bar_x, widths):
    bands = "".join(
        f'<rect x="770" y="{y}" width="380" height="{h}" fill="{fill}"/>'
        for y, h, fill in [(30, 90, "#EAE5DA"), (120, 70, "#DFD8C9"), (190, 100, "#D2CBBB")]
    )
    bars = "".join(
        f'<rect x="{bar_x}" y="{y}" width="{w}" height="7" rx="3.5" fill="#BDB5A1"/>'
        for y, w in zip([94, 212, 234], widths)
    )
    return bands + bars


weak_shaft = "".join(f'<rect x="1036" y="{y}" width="8" height="14" fill="{INK}"/>' for y in [190, 212, 234, 256])
dig_vignette = f"""    <defs>
      <clipPath id="panel"><rect x="770" y="50" width="380" height="268" rx="16"/></clipPath>
      <clipPath id="beforeSide"><path d="M770 50 H950 L905 262 H770 Z"/></clipPath>
      <clipPath id="afterSide"><path d="M950 50 H1150 V262 H905 Z"/></clipPath>
      <pattern id="undug" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="10" height="10" fill="{SURFACE}"/><rect width="3" height="10" fill="{RULE}"/></pattern>
    </defs>
    <g clip-path="url(#panel)">
      <g clip-path="url(#beforeSide)">
        {rock(784, [92, 72, 108])}
        <text x="782" y="160" class="m ink" font-size="11" font-weight="600">return price * 0.10</text>
      </g>
      <g clip-path="url(#afterSide)"><g class="slip">
        {rock(965, [128, 84, 116])}
        <text x="945" y="160" class="m ink was alt" font-size="11" font-weight="600">return price * 0.10</text>
        <text x="945" y="160" class="m ink now" font-size="11" font-weight="600">return price * 0.15</text>
      </g></g>
      <rect x="770" y="262" width="380" height="56" fill="url(#undug)"/>
    </g>
    <path d="M950 50 L905 262" fill="none" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>
    <text x="784" y="76" class="m ink" font-size="10" font-weight="700" letter-spacing="1.2">BASE</text>
    <text x="1136" y="76" text-anchor="end" class="m ink" font-size="10" font-weight="700" letter-spacing="1.2">HEAD</text>
    <g class="bore b1"><rect x="956" y="190" width="8" height="88" fill="{ACCENT}"/></g>
    <g class="bore b2">{weak_shaft}</g>
    <g class="bore b3"><rect x="1111" y="190" width="8" height="88" fill="{PAPER}" stroke="{INK}" stroke-width="2"/></g>
    <rect x="784" y="278" width="116" height="22" rx="11" fill="{PAPER}"/>
    <text x="842" y="293" text-anchor="middle" class="m mut" font-size="9.5" font-weight="700" letter-spacing=".6">UNDUG GROUND</text>
    <g class="t1"><rect x="930" y="278" width="60" height="22" rx="11" fill="{ACCENT}"/><text x="960" y="293" text-anchor="middle" class="m" fill="#FFFFFF" font-size="9.5" font-weight="700" letter-spacing=".6">STRONG</text></g>
    <g class="t2"><rect x="1010" y="278" width="60" height="22" rx="11" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><text x="1040" y="293" text-anchor="middle" class="m ink" font-size="9.5" font-weight="700" letter-spacing=".6">WEAK</text></g>
    <g class="t3"><rect x="1085" y="278" width="60" height="22" rx="11" fill="{PAPER}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="4 4"/><text x="1115" y="293" text-anchor="middle" class="m mut" font-size="9.5" font-weight="700" letter-spacing=".6">NONE</text></g>
    <rect x="770" y="50" width="380" height="268" rx="16" fill="none" stroke="{INK}" stroke-width="3"/>
    <text x="960" y="346" text-anchor="middle" class="m mut" font-size="10.5" letter-spacing="1.2">FAULT = CHANGE · SHAFT = POSSIBLE TEST LINK</text>"""

wide(
    "change-archaeologist", "Change Archaeologist", "STATION 08 · GIT HISTORY · TERMINUS", (ACCENT, 5),
    ["See how a function changed between two Git versions,", "and whether its tests moved with it."],
    ["Reads both versions as syntax trees, then separates what it saw from what",
     "that suggests and what it can't know. No AI, and it never runs your code."],
    "TYPESCRIPT · TS-MORPH · REACT + VITE · MONACO · NODE CLI",
    [("6", "CHANGE PATTERNS"), ("4", "LINK STATUSES"), ("0", "AI CALLS")],
    dig_vignette, dig_style,
    "Local-first static analysis that compares a function across two Git revisions and looks for matching changes in its tests, separating evidence from inference.",
)
print("cards written to", OUT)
