"""Builds the profile from one list of stations. Run: python scripts/build.py

Adding a project: draw its card in scripts/cards.py, add one entry to STATIONS
below, run this script. It regenerates the cards, the route map, the footer,
the earlier-station signs, and the stations block in README.md. The four
newest stations are shown as full cards; older ones become small linked
signs, five to a row, so the README barely grows as the line gets longer.
(A collapsible <details> section was tried and dropped: GitHub always draws
its disclosure arrow, and READMEs cannot style it away.)
"""
import math
import re
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
USER = "rknishanth152-lgtm"

PAPER, SURFACE, INK, MUTED, ACCENT = "#F4F1EA", "#EAE5DA", "#14161A", "#5F6168", "#2F55E4"
FONTS = """
    .d{font-family:'Segoe UI Variable Display','Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif}
    .m{font-family:ui-monospace,SFMono-Regular,'Cascadia Mono',Consolas,Menlo,monospace}
    .ink{fill:#14161A}.mut{fill:#5F6168}"""

FEATURED = 4

STATIONS = [
    dict(place="SHOP", title="Smart Billing", card="smart-billing", repo="smart-billing-system",
         alt="Smart Billing. Java Swing billing and inventory for Shree Annapurna Edible Oil Company."),
    dict(place="CLASSROOM", title="SpaceXR", card="spacexr", repo="SpaceXR",
         alt="SpaceXR. An interactive Solar System in the browser with WebXR."),
    dict(place="FIELD", title="FarmSense AI", card="farmsense-ai", repo="farmsense-ai",
         alt="FarmSense AI. Crop disease diagnosis from a photo, plus irrigation and yield planning."),
    dict(place="SKY", title="WeatherGuard AI", card="weatherguard-ai", repo="WeatherGuard-AI",
         alt="WeatherGuard AI. Random Forest rain prediction with a four-tier advisory."),
    dict(place="BROWSER", title="PhishSentinel", card="phishsentinel", repo="PhishSentinel",
         alt="PhishSentinel. XGBoost phishing URL detection with a Chrome extension."),
    dict(place="PHONE", title="JanKavach", card="jankavach", repo="JanKavach",
         alt="JanKavach. A Telegram bot that flags scam texts and voice notes."),
    dict(place="HOME", title="Family Finance", card="family-finance", repo="family-finance-manager",
         alt="Family Finance. Offline-first Android money manager in Tamil and English, kept to the paisa."),
    dict(place="GIT HISTORY", title="Change Archaeologist", card="change-archaeologist", repo="change-archaeologist",
         alt="Change Archaeologist. Shows how a function changed between two Git versions and whether its tests moved with it."),
    dict(place="LIBRARY", title="PaperPilot", card="paperpilot", repo="paperpilot",
         alt="PaperPilot. Answers questions about research papers with every sentence linked to the passage it quotes."),
]

WORDS = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen".split()

# ---------------------------------------------------------------- route map
# The line runs left to right, loops down, runs back, and so on: five stations
# per row, so it only ever grows downwards.
PER_ROW, X0, SPACING, LEFT, RIGHT, TOP, GAP = 5, 170, 215, 110, 1090, 190, 140
R = GAP / 2
SPEED = 150  # px per second for the train


def slot(i):
    row, k = divmod(i, PER_ROW)
    x = X0 + k * SPACING if row % 2 == 0 else X0 + (PER_ROW - 1 - k) * SPACING
    return x, TOP + row * GAP


def walk(start, start_index, stop_index):
    """Path commands and distance from point `start` (at station start_index) to station stop_index."""
    (x, y), cmds, dist, marks = start, [], 0.0, {}
    for i in range(start_index + 1, stop_index + 1):
        tx, ty = slot(i)
        if ty != y:
            end = RIGHT if (i // PER_ROW - 1) % 2 == 0 else LEFT
            cmds.append(f"H{end}")
            dist += abs(end - x)
            cmds.append(f"A{R:g} {R:g} 0 0 {1 if end == RIGHT else 0} {end} {ty}")
            dist += math.pi * R
            x, y = end, ty
        cmds.append(f"H{tx}")
        dist += abs(tx - x)
        x = tx
        marks[i] = dist
    return cmds, dist, marks


def route():
    n = len(STATIONS)
    fx, fy = slot(0)
    cmds, length, marks = walk((LEFT, fy), -1, n - 1)
    marks = {i: d for i, d in marks.items()}
    line = f"M{LEFT} {fy} " + " ".join(cmds)
    lx, ly = slot(n - 1)
    nx, ny = slot(n)
    next_cmds, _, _ = walk((lx, ly), n - 1, n)
    dotted = f"M{lx} {ly} " + " ".join(next_cmds)

    travel = length / SPEED
    dur = travel / 0.94
    rows = n // PER_ROW + 1
    height = int(TOP + (rows - 1) * GAP + 104)
    dash = math.ceil(length)
    word = WORDS[n].upper() if n < len(WORDS) else str(n)

    pings, dots, labels = [], [], []
    for i, s in enumerate(STATIONS):
        x, y = slot(i)
        last = i == n - 1
        r = 14 if last else 11
        pings.append(f'<circle cx="{x}" cy="{y}" r="{r}" class="ping" style="animation-delay:{1.9 + marks[i] / SPEED:.2f}s"/>')
        ring = f' r="15" stroke="{ACCENT}" stroke-width="6"' if last else ' r="11"'
        dots.append(f'<circle cx="{x}" cy="{y}"{ring} class="st" style="animation-delay:{.3 + .12 * i:.2f}s"/>')
        labels.append(
            f'<g class="lb" style="animation-delay:{.5 + .12 * i:.2f}s">'
            f'<text x="{x}" y="{y + 38}" class="d ink" font-size="17" font-weight="{700 if last else 600}">{s["title"]}</text>'
            f'<text x="{x}" y="{y + 60}" class="m mut" font-size="11.5" letter-spacing="1.2">{i + 1:02d} · {s["place"]}</text></g>'
        )
    nl = "\n    "
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="t d">
  <title id="t">The line so far</title>
  <desc id="d">{word.capitalize()} projects drawn as stations on one line: {", ".join(f'{s["title"]} ({s["place"].lower()})' for s in STATIONS)}.</desc>
  <defs>
    <path id="line" d="{line}"/>
  </defs>
  <style>{FONTS}
    @keyframes draw{{from{{stroke-dashoffset:{dash}}}to{{stroke-dashoffset:0}}}}
    @keyframes up{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
    @keyframes pop{{from{{opacity:0;transform:scale(.2)}}to{{opacity:1;transform:none}}}}
    @keyframes pass{{0%{{opacity:.9;transform:scale(1)}}9%{{opacity:0;transform:scale(2.6)}}100%{{opacity:0;transform:scale(2.6)}}}}
    @keyframes breathe{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
    .route{{stroke-dasharray:{dash};animation:draw 2s cubic-bezier(.6,0,.2,1) .2s both}}
    .h{{animation:up .7s ease-out both}}
    .st{{transform-box:fill-box;transform-origin:center;animation:pop .45s cubic-bezier(.3,1.6,.5,1) both}}
    .lb{{animation:up .6s ease-out both}}
    .ping{{transform-box:fill-box;transform-origin:center;opacity:0;animation:pass {dur:.2f}s ease-out infinite}}
    .next{{animation:breathe 2.4s ease-in-out infinite}}
    @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.ping{{opacity:0}}}}
  </style>

  <rect width="1200" height="{height}" rx="28" fill="{PAPER}"/>

  <g class="h">
    <text x="60" y="72" class="d ink" font-size="32" font-weight="700" letter-spacing="-.8">The line so far</text>
    <text x="60" y="102" class="m mut" font-size="12.5" letter-spacing="1.2">{word} PROJECTS · {word} PLACES THEY RUN</text>
  </g>
  <g class="h" style="animation-delay:.15s">
    <circle cx="806" cy="67" r="8" fill="{PAPER}" stroke="{ACCENT}" stroke-width="4"/>
    <text x="822" y="71.5" class="m mut" font-size="12" letter-spacing="1.2">NEWEST</text>
    <circle cx="930" cy="67" r="8" fill="{PAPER}" stroke="{MUTED}" stroke-width="2.5" stroke-dasharray="3 4"/>
    <text x="946" y="71.5" class="m mut" font-size="12" letter-spacing="1.2">NEXT · BEING BUILT</text>
  </g>

  <path d="{dotted}" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" stroke-dasharray="2 18" opacity=".55"/>
  <use xlink:href="#line" class="route" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- pings fire as the train passes: 1.9s start + distance / {SPEED}px per second -->
  <g fill="none" stroke="{ACCENT}" stroke-width="3">
    {nl.join(pings)}
  </g>
  <g fill="{PAPER}" stroke="{INK}" stroke-width="4.5">
    {nl.join(dots)}
  </g>
  <g class="next"><circle cx="{nx}" cy="{ny}" r="11" fill="{PAPER}" stroke="{MUTED}" stroke-width="3" stroke-dasharray="3 4"/></g>
  <text x="{nx}" y="{ny + 38}" text-anchor="middle" class="m mut" font-size="11.5" letter-spacing="1.2">NEXT STATION</text>

  <g text-anchor="middle">
    {nl.join(labels)}
  </g>

  <g opacity="0">
    <set attributeName="opacity" to="1" begin="1.9s" fill="freeze"/>
    <rect x="-20" y="-8" width="40" height="16" rx="8" fill="{ACCENT}"/>
    <rect x="6" y="-3.5" width="8" height="7" rx="2" fill="{PAPER}"/>
    <animateMotion dur="{dur:.2f}s" begin="1.9s" repeatCount="indefinite" rotate="auto" keyPoints="0;1;1" keyTimes="0;.94;1" calcMode="linear">
      <mpath xlink:href="#line"/>
    </animateMotion>
  </g>
</svg>
"""
    (ASSETS / "route.svg").write_text(svg, encoding="utf-8")


# ---------------------------------------------------------------- footer
def footer():
    last = STATIONS[-1]
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="170" viewBox="0 0 1200 170" role="img" aria-labelledby="t d">
  <title id="t">Next station</title>
  <desc id="d">The line continues past {last["title"]} towards the next project. Thanks for riding.</desc>
  <style>{FONTS}
    @keyframes run{{0%{{transform:translateX(0);opacity:0}}6%{{opacity:1}}88%{{opacity:1}}100%{{transform:translateX(1000px);opacity:0}}}}
    @keyframes breathe{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
    .train{{animation:run 7s cubic-bezier(.45,0,.35,1) infinite}}
    .next{{animation:breathe 2.4s ease-in-out infinite}}
    @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
  </style>
  <rect width="1200" height="170" rx="28" fill="{PAPER}"/>
  <path d="M80 70 H940" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>
  <path d="M940 70 H1110" stroke="{INK}" stroke-width="9" stroke-linecap="round" stroke-dasharray="2 18"/>
  <circle cx="80" cy="70" r="15" fill="{PAPER}" stroke="{ACCENT}" stroke-width="6"/>
  <circle cx="1120" cy="70" r="11" fill="{PAPER}" stroke="{INK}" stroke-width="4.5" class="next"/>
  <g class="train"><rect x="94" y="62" width="40" height="16" rx="8" fill="{ACCENT}"/><rect x="120" y="66.5" width="8" height="7" rx="2" fill="{PAPER}"/></g>
  <text x="80" y="124" class="m mut" font-size="12" letter-spacing="1.3">{len(STATIONS):02d} · {last["place"]}</text>
  <text x="1120" y="124" text-anchor="end" class="m mut" font-size="12" letter-spacing="1.3">NEXT STATION · BEING BUILT</text>
  <text x="600" y="130" text-anchor="middle" class="d ink" font-size="20" font-weight="600">Thanks for riding the line.</text>
</svg>
"""
    (ASSETS / "footer.svg").write_text(svg, encoding="utf-8")


# ---------------------------------------------------------------- earlier stations
SIGNS_PER_ROW = 5


def earlier_label(count):
    """Section heading in the same style as label-toolkit.svg."""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="120" viewBox="0 0 1200 120" role="img" aria-labelledby="t">
  <title id="t">Earlier stations</title>
  <style>{FONTS}
    @keyframes up{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
    @keyframes grow{{from{{transform:scaleX(0)}}to{{transform:none}}}}
    .h{{animation:up .7s ease-out both}}
    .bar{{transform-box:fill-box;transform-origin:left;animation:grow 1s cubic-bezier(.6,0,.2,1) .2s both}}
    @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
  </style>
  <rect width="1200" height="120" rx="28" fill="{PAPER}"/>
  <g class="h">
    <text x="60" y="62" class="d ink" font-size="32" font-weight="700" letter-spacing="-.8">Earlier stations</text>
    <text x="60" y="90" class="m mut" font-size="12.5" letter-spacing="1.2">01–{count:02d} · EACH SIGN OPENS ITS REPOSITORY</text>
  </g>
  <rect x="360" y="56" width="780" height="9" rx="4.5" fill="{INK}" class="bar"/>
  <circle cx="1140" cy="60.5" r="11" fill="{PAPER}" stroke="{MUTED}" stroke-width="4.5"/>
</svg>
"""
    (ASSETS / "label-earlier.svg").write_text(svg, encoding="utf-8")


def sign(i, s):
    """A small station sign: number, place, name and an arrow. Shown at about 160px wide."""
    title = s["title"]
    size = min(30, round(224 / (0.56 * len(title)), 1))
    delay = .08 * (i % SIGNS_PER_ROW)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="300" height="128" viewBox="0 0 300 128" role="img" aria-labelledby="t">
  <title id="t">Station {i + 1:02d}, {s["place"].title()}: {title}</title>
  <style>{FONTS}
    @keyframes up{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
    @keyframes nudge{{0%,100%{{transform:none}}50%{{transform:translateX(5px)}}}}
    @keyframes ping{{0%{{opacity:.9;transform:scale(1)}}30%,100%{{opacity:0;transform:scale(2.4)}}}}
    .h{{animation:up .6s ease-out {delay:.2f}s both}}
    .arrow{{animation:nudge 1.8s ease-in-out infinite}}
    .ping{{transform-box:fill-box;transform-origin:center;opacity:0;animation:ping 4s ease-out {1 + .7 * i:.1f}s infinite}}
    @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.ping{{opacity:0}}}}
  </style>
  <rect width="300" height="128" rx="20" fill="{PAPER}"/>
  <g class="h">
    <circle cx="32" cy="38" r="9" fill="none" stroke="{ACCENT}" stroke-width="3" class="ping"/>
    <circle cx="32" cy="38" r="9" fill="{PAPER}" stroke="{INK}" stroke-width="4.5"/>
    <text x="52" y="44" class="m mut" font-size="16" letter-spacing="1.4">{i + 1:02d} · {s["place"]}</text>
    <text x="22" y="96" class="d ink" font-size="{size:g}" font-weight="700" letter-spacing="-.6">{title}</text>
    <g class="arrow"><text x="278" y="96" text-anchor="end" class="d" fill="{ACCENT}" font-size="24" font-weight="700">→</text></g>
  </g>
</svg>
"""
    (ASSETS / "signs").mkdir(exist_ok=True)
    (ASSETS / "signs" / f"{s['card']}.svg").write_text(svg, encoding="utf-8")


# ---------------------------------------------------------------- README block
def card_link(i, s):
    return (f'<a href="https://github.com/{USER}/{s["repo"]}"><img src="assets/cards/{s["card"]}.svg" width="49%" '
            f'alt="Station {i + 1:02d}, {s["place"].title()}: {s["alt"]}"/></a>')


def pairs(items):
    return "\n\n".join("\n".join(card_link(i, s) for i, s in items[k:k + 2]) for k in range(0, len(items), 2))


def sign_link(i, s):
    return (f'<a href="https://github.com/{USER}/{s["repo"]}"><img src="assets/signs/{s["card"]}.svg" width="19%" '
            f'alt="Station {i + 1:02d}, {s["place"].title()}: {s["title"]}"/></a>')


def readme(featured, older):
    block = pairs(featured)
    if older:
        rows = "\n\n".join("\n".join(sign_link(i, s) for i, s in older[k:k + SIGNS_PER_ROW])
                           for k in range(0, len(older), SIGNS_PER_ROW))
        block += f"""

<br/>

<img src="assets/label-earlier.svg" width="100%" alt="Earlier stations"/>

<br/><br/>

{rows}"""
    p = ROOT / "README.md"
    text = p.read_text(encoding="utf-8")
    new, count = re.subn(r"(<!-- stations:start -->\r?\n).*?(<!-- stations:end -->)",
                         lambda m: m.group(1) + block + "\n" + m.group(2), text, flags=re.S)
    assert count == 1, "README needs one <!-- stations:start --> ... <!-- stations:end --> block"
    p.write_text(new, encoding="utf-8")


if __name__ == "__main__":
    runpy.run_path(str(ROOT / "scripts" / "cards.py"))
    numbered = list(enumerate(STATIONS))
    featured = numbered[::-1][:FEATURED]
    older = numbered[: max(len(STATIONS) - FEATURED, 0)]
    route()
    footer()
    if older:
        earlier_label(len(older))
    for i, s in older:
        sign(i, s)
    readme(featured, older)
    print(f"built {len(STATIONS)} stations: {len(featured)} featured, {len(older)} earlier")
