"""Regenerate assets/header.svg.

    uv run --with 'fonttools[woff]' python scripts/gen_header.py

Edit the content constants below, then re-run. The script subsets Maple Mono
NF to only the glyphs used, embeds them as base64 woff2 (GitHub blocks
external font loads in README SVGs), and recomputes the typing animation from
the font's real per-character advances.
"""
import base64, io
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

FONTS = "/Users/andy/Library/Fonts/MapleMono-NF-{}.ttf"
OUT = "/Users/andy/Projects/Andy8647/assets/header.svg"

# ---- content -------------------------------------------------------------
# Nerd Font glyphs, all verified present in MapleMono-NF. Their advance is
# one cell (600 units) but the ink runs to ~1130, i.e. nearly two cells --
# terminals reserve a double cell for that, SVG does not. Hence two spaces
# after each icon, which SVG only honours under xml:space=preserve.
ICON_TERM  = "\uf489"  # terminal
ICON_AGENT = "\uf085"  # cogs
ICON_CTX   = "\uf1c0"  # database
ICON_MCP   = "\uf1b3"  # cubes
ICON_REL   = "\uf021"  # refresh -- retry/resume, which is what the work is

CMD     = "cat /etc/andy/identity"
OUTPUT  = "Andy Luo \u2014 builds agents, and keeps them running"
ACCENT  = (f"{ICON_AGENT}  Agents \u00b7 {ICON_CTX}  Context engineering \u00b7 "
           f"{ICON_MCP}  MCP \u00b7 {ICON_REL}  Reliability")
COMMENT = "# the second half is where the work is"
TITLE   = f"{ICON_TERM}  andy@shanghai ~"
PROMPT  = "❯"

# Icon glyphs are not guaranteed to share the 0.6em advance of the Latin
# set, so widths are measured per character from the font's own hmtx.
_metric_cache = {}


def advances(text, size, style="Regular"):
    if style not in _metric_cache:
        f = TTFont(FONTS.format(style))
        _metric_cache[style] = (f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    cmap, hmtx, upm = _metric_cache[style]
    out = []
    for ch in text:
        gname = cmap.get(ord(ch))
        adv = hmtx[gname][0] if gname else int(upm * 0.6)
        out.append(adv / upm * size)
    return out


def typing(cid, x, y, text, size, dur, begin, style="Regular"):
    """Discrete clip-path reveal, one step per character, real advances."""
    adv = advances(text, size, style)
    n = len(text)
    cum, acc = [0.0], 0.0
    for a in adv:
        acc += a
        cum.append(acc)
    w = acc
    vals = [round(v, 2) for v in cum]
    times = [round(i / n, 3) for i in range(n + 1)]
    return (
        f'    <clipPath id="{cid}"><rect x="{x}" y="{y}" height="{round(size*1.6)}" width="0">\n'
        f'      <animate attributeName="width" from="0" to="{round(w,2)}" dur="{dur}s" '
        f'begin="{begin}s" fill="freeze" calcMode="discrete" '
        f'values="{";".join(str(v) for v in vals)}" '
        f'keyTimes="{";".join(str(t) for t in times)}" />\n'
        f'    </rect></clipPath>\n'
    )


def embed(style_name, chars, weight, italic):
    f = TTFont(FONTS.format(style_name))
    opts = Options()
    opts.layout_features = []
    opts.desubroutinize = True
    opts.notdef_outline = False
    opts.recalc_bounds = True
    sub = Subsetter(options=opts)
    sub.populate(text="".join(sorted(set(chars))))
    sub.subset(f)
    f.flavor = "woff2"
    buf = io.BytesIO()
    f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    style = "italic" if italic else "normal"
    return (
        f"    @font-face {{ font-family: 'MapleMono'; font-weight: {weight}; "
        f"font-style: {style}; src: url(data:font/woff2;base64,{b64}) format('woff2'); }}\n"
    ), len(b64)


regular_chars = CMD + OUTPUT + ACCENT + TITLE
face_r, n_r = embed("Regular", regular_chars, 400, False)
face_b, n_b = embed("Bold", PROMPT, 700, False)
face_i, n_i = embed("Italic", COMMENT, 400, True)

clips = (
    typing("c1", 44, 54, CMD, 15, 1.6, 0.5)
    + typing("c2", 24, 84, OUTPUT, 15, 2.0, 2.5)
    + '    <clipPath id="c3"><rect x="24" y="119" height="24" width="0">\n'
      '      <animate attributeName="width" from="0" to="9" dur="0.08s" begin="5s" fill="freeze" />\n'
      '    </rect></clipPath>\n'
    + typing("c4", 44, 119, ACCENT, 15, 1.8, 5.2)
    + typing("c5", 24, 150, COMMENT, 14, 2.2, 7.5, style="Italic")
)

FAMILY = "'MapleMono', 'Maple Mono NF', 'Maple Mono', ui-monospace, 'SF Mono', 'Courier New', monospace"

svg = f"""<svg width="800" height="220" xmlns="http://www.w3.org/2000/svg">
  <defs>
{clips}  </defs>

  <style>
{face_r}{face_b}{face_i}
    .terminal-bg {{ fill: #0d1117; }}
    .title-bar {{ fill: #161b22; }}
    .dot-red {{ fill: #ff5f57; }}
    .dot-yellow {{ fill: #febc2e; }}
    .dot-green {{ fill: #28c840; }}
    .title-text {{ fill: #8b949e; font-family: {FAMILY}; font-size: 12px; }}
    .prompt {{ fill: #58a6ff; font-family: {FAMILY}; font-size: 15px; font-weight: 700; }}
    .command {{ fill: #c9d1d9; font-family: {FAMILY}; font-size: 15px; }}
    .output {{ fill: #7ee787; font-family: {FAMILY}; font-size: 15px; }}
    .comment {{ fill: #8b949e; font-family: {FAMILY}; font-size: 14px; font-style: italic; }}
    .accent {{ fill: #d2a8ff; font-family: {FAMILY}; font-size: 15px; }}
  </style>

  <!-- Terminal background -->
  <rect class="terminal-bg" width="800" height="220" rx="12" />

  <!-- Title bar -->
  <rect class="title-bar" width="800" height="36" rx="12" />
  <rect class="title-bar" width="800" height="16" y="20" />

  <!-- Window controls -->
  <circle class="dot-red" cx="20" cy="18" r="6" />
  <circle class="dot-yellow" cx="40" cy="18" r="6" />
  <circle class="dot-green" cx="60" cy="18" r="6" />
  <text class="title-text" x="370" y="22" text-anchor="middle" xml:space="preserve">{TITLE}</text>

  <!-- Line 1: prompt + command -->
  <text class="prompt" x="24" y="72" opacity="0">{PROMPT}<set attributeName="opacity" to="1" begin="0.3s" fill="freeze" /></text>
  <text class="command" x="44" y="72" clip-path="url(#c1)">{CMD}</text>

  <!-- Line 2: output -->
  <text class="output" x="24" y="102" clip-path="url(#c2)">{OUTPUT}</text>

  <!-- Line 3: prompt + focus -->
  <text class="prompt" x="24" y="137" clip-path="url(#c3)">{PROMPT}</text>
  <text class="accent" x="44" y="137" clip-path="url(#c4)" xml:space="preserve">{ACCENT}</text>

  <!-- Line 4: comment -->
  <text class="comment" x="24" y="170" clip-path="url(#c5)">{COMMENT}</text>

  <!-- Blinking cursor -->
  <rect x="24" y="180" width="10" height="16" fill="#58a6ff" opacity="0">
    <set attributeName="opacity" to="1" begin="10s" fill="freeze" />
    <animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.4;0.5;0.9;1" dur="1s" begin="10s" repeatCount="indefinite" />
  </rect>
</svg>
"""

open(OUT, "w").write(svg)
print(f"wrote {OUT}")
print(f"font payload (base64 chars): regular={n_r} bold={n_b} italic={n_i}")
for label, t, size, x, st in [("cmd", CMD, 15, 44, "Regular"), ("output", OUTPUT, 15, 24, "Regular"),
                              ("accent", ACCENT, 15, 44, "Regular"), ("comment", COMMENT, 14, 24, "Italic"),
                              ("title", TITLE, 12, 370, "Regular")]:
    end = x + sum(advances(t, size, st))
    flag = "  <-- OVERFLOW" if end > 800 else ""
    print(f"  {label:8} {len(t):3} chars -> ends at x={end:.0f}{flag}")
