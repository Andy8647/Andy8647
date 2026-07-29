"""Regenerate assets/header.svg.

    uv run --with 'fonttools[woff]' python scripts/gen_header.py

Edit LINES below, then re-run. The script subsets Maple Mono NF to only the
glyphs used, embeds them as base64 woff2 (GitHub blocks external font loads in
README SVGs, so naming the family alone would only work for people who happen
to have it installed), and derives each typing animation from the font's real
per-character advances.

Two things here are easy to get wrong:

* Nerd Font icons have a one-cell advance (600) but ink running to ~1150, i.e.
  nearly two cells. Terminals reserve a double cell for them; SVG does not.
  Hence the padding spaces after each icon.
* SVG collapses runs of whitespace unless xml:space="preserve" is set, which
  silently undoes that padding.
"""

import base64, io
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

FONTS = "/Users/andy/Library/Fonts/MapleMono-NF-{}.ttf"
OUT = "/Users/andy/Projects/Andy8647/assets/header.svg"

W, H = 800, 300

# ---- Catppuccin Mocha ----------------------------------------------------
C = {
    "base": "#1e1e2e", "mantle": "#181825", "surface0": "#313244",
    "text": "#cdd6f4", "subtext1": "#bac2de", "subtext0": "#a6adc8",
    "overlay0": "#6c7086", "overlay1": "#7f849c",
    "blue": "#89b4fa", "lavender": "#b4befe", "sky": "#89dceb",
    "green": "#a6e3a1", "yellow": "#f9e2af", "peach": "#fab387",
    "red": "#f38ba8", "mauve": "#cba6f7",
}

# Syntax roles, so the terminal reads like a highlighted shell session.
ROLE = {
    "prompt":  (C["green"],    700, False),
    "cmd":     (C["blue"],     400, False),   # command name
    "arg":     (C["text"],     400, False),   # paths and positional args
    "flag":    (C["peach"],    400, False),
    "str":     (C["green"],    400, False),
    "num":     (C["peach"],    400, False),
    "name":    (C["yellow"],   700, False),
    "out":     (C["subtext1"], 400, False),
    "accent":  (C["mauve"],    400, False),
    "icon":    (C["sky"],      400, False),
    "ok":      (C["green"],    400, False),
    "arrow":   (C["overlay1"], 400, False),
    "dim":     (C["subtext0"], 400, False),
    "comment": (C["overlay0"], 400, True),
}

# Nerd Font glyphs, all verified present in MapleMono-NF.
I_TERM  = ""  # terminal
I_AGENT = ""  # cogs
I_CTX   = ""  # database
I_MCP   = ""  # cubes
I_REL   = ""  # refresh -- retry/resume, which is what the work is
PAD = "  "          # clears the icon ink; needs xml:space="preserve"

TITLE = f"{I_TERM}{PAD}andy@shanghai ~"

# (y, font-size, [(text, role)], begin, dur)
LINES = [
    (72, 15, [("❯ ", "prompt"), ("cat", "cmd"), (" ~/.andy/identity", "arg")], 0.3, 1.0),
    (100, 15, [("Andy Luo", "name"),
               (" — builds agents, and keeps them running", "out")], 1.5, 1.2),
    (134, 15, [("❯ ", "prompt"), ("agent", "cmd"), (" run", "arg"),
               (" --task", "flag"), (' "ship it"', "str"),
               (" --hours", "flag"), (" 4", "num")], 3.0, 1.3),
    (162, 15, [(I_AGENT, "icon"), (f"{PAD}Agents", "accent"), ("  ·  ", "dim"),
               (I_CTX, "icon"), (f"{PAD}Context engineering", "accent"), ("  ·  ", "dim"),
               (I_MCP, "icon"), (f"{PAD}MCP", "accent"), ("  ·  ", "dim"),
               (I_REL, "icon"), (f"{PAD}Reliability", "accent")], 4.5, 1.5),
    (192, 15, [("✔ ", "ok"), ("rate limit hit ", "out"), ("→", "arrow"),
               (" waited for reset ", "out"), ("→", "arrow"),
               (" resumed", "out")], 6.2, 1.3),
    (220, 15, [("✔ ", "ok"), ("plan split per task ", "out"), ("→", "arrow"),
               (" context stayed under budget", "out")], 7.7, 1.4),
    (254, 14, [("# the second half is where the work is", "comment")], 9.3, 1.2),
]

CURSOR_AT = 10.8

_metrics = {}


def _font(style):
    if style not in _metrics:
        f = TTFont(FONTS.format(style))
        _metrics[style] = (f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    return _metrics[style]


def advances(text, size, style):
    cmap, hmtx, upm = _font(style)
    out = []
    for ch in text:
        g = cmap.get(ord(ch))
        out.append((hmtx[g][0] if g else int(upm * 0.6)) / upm * size)
    return out


def style_of(role):
    _, weight, italic = ROLE[role]
    return "Italic" if italic else ("Bold" if weight >= 700 else "Regular")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


clips, texts = [], []
chars = {"Regular": set(TITLE), "Bold": set(), "Italic": set()}

for idx, (y, size, segs, begin, dur) in enumerate(LINES, start=1):
    adv = []
    for text, role in segs:
        chars[style_of(role)] |= set(text)
        adv += advances(text, size, style_of(role))
    cum, acc = [0.0], 0.0
    for a in adv:
        acc += a
        cum.append(acc)
    n = len(adv)
    cid = f"c{idx}"
    clips.append(
        f'    <clipPath id="{cid}"><rect x="24" y="{y - 15}" height="{round(size * 1.5)}" width="0">'
        f'<animate attributeName="width" from="0" to="{round(acc, 2)}" dur="{dur}s" begin="{begin}s" '
        f'fill="freeze" calcMode="discrete" '
        f'values="{";".join(str(round(v, 2)) for v in cum)}" '
        f'keyTimes="{";".join(str(round(i / n, 4)) for i in range(n + 1))}" />'
        f'</rect></clipPath>'
    )
    spans = "".join(f'<tspan class="{r}">{esc(t)}</tspan>' for t, r in segs)
    texts.append(
        f'  <text x="24" y="{y}" font-size="{size}" clip-path="url(#{cid})" '
        f'xml:space="preserve">{spans}</text>'
    )


def face(style, weight, italic):
    used = chars[style]
    if not used:
        return ""
    f = TTFont(FONTS.format(style))
    opts = Options()
    opts.layout_features = []
    opts.desubroutinize = True
    opts.notdef_outline = False
    sub = Subsetter(options=opts)
    sub.populate(text="".join(sorted(used)))
    sub.subset(f)
    f.flavor = "woff2"
    buf = io.BytesIO()
    f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return (f"    @font-face {{ font-family: 'MapleMono'; font-weight: {weight}; "
            f"font-style: {'italic' if italic else 'normal'}; "
            f"src: url(data:font/woff2;base64,{b64}) format('woff2'); }}\n")


faces = face("Regular", 400, False) + face("Bold", 700, False) + face("Italic", 400, True)
FAMILY = "'MapleMono', 'Maple Mono NF', ui-monospace, 'SF Mono', monospace"
roles_css = "\n".join(
    f"    .{k} {{ fill: {v[0]}; font-weight: {v[1]};"
    f"{' font-style: italic;' if v[2] else ''} }}" for k, v in ROLE.items()
)
NL = chr(10)

svg = f"""<svg width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
{NL.join(clips)}
  </defs>

  <style>
{faces}
    text {{ font-family: {FAMILY}; }}
{roles_css}
  </style>

  <rect width="{W}" height="{H}" rx="12" fill="{C['base']}" />
  <rect width="{W}" height="36" rx="12" fill="{C['mantle']}" />
  <rect width="{W}" height="16" y="20" fill="{C['mantle']}" />
  <rect width="{W}" height="1" y="36" fill="{C['surface0']}" />

  <circle cx="20" cy="18" r="6" fill="{C['red']}" />
  <circle cx="40" cy="18" r="6" fill="{C['yellow']}" />
  <circle cx="60" cy="18" r="6" fill="{C['green']}" />
  <text x="{W // 2}" y="22" font-size="12" text-anchor="middle" fill="{C['subtext0']}" xml:space="preserve">{esc(TITLE)}</text>

{NL.join(texts)}

  <rect x="24" y="272" width="10" height="16" fill="{C['lavender']}" opacity="0">
    <set attributeName="opacity" to="1" begin="{CURSOR_AT}s" fill="freeze" />
    <animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.4;0.5;0.9;1"
             dur="1s" begin="{CURSOR_AT}s" repeatCount="indefinite" />
  </rect>
</svg>
"""

open(OUT, "w", encoding="utf-8").write(svg)
print(f"wrote {OUT}")
for i, (y, size, segs, _, _) in enumerate(LINES, start=1):
    end = 24 + sum(sum(advances(t, size, style_of(r))) for t, r in segs)
    print(f"  line{i} ends x={end:6.0f}{'   <-- OVERFLOW' if end > W - 16 else ''}")
