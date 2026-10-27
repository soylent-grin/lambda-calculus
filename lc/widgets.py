import re

from lc.theme import *

_TOKEN = re.compile(
    r"//.*?$|--.*?$|\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|\b\d+\b|\b[A-Za-z_][A-Za-z0-9_]*\b|=>|->|\s+|.",
    re.M,
)
_KW = {
    "js": {"const", "let", "function", "return", "if", "else", "while", "true", "false", "switch", "case", "type"},
    "hs": {"if", "then", "else", "let", "in", "data", "case", "of", "where"},
    "go": {"func", "var", "return", "if", "else", "package"},
}
_TY = {"int", "string", "bool"}


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


_SPAN = re.compile(r"(\*[^*]+\*|`[^`]+`)")


def _markup(text):
    chunks = []
    for part in _SPAN.split(text):
        if len(part) >= 2 and part[0] == part[-1] == "*":
            chunks.append(f'<span fgcolor="{GOLD}">{esc(part[1:-1])}</span>')
        elif len(part) >= 2 and part[0] == part[-1] == "`":
            chunks.append(f'<span font_family="{MONO}" fgcolor="{SKY}">{esc(part[1:-1])}</span>')
        else:
            chunks.append(esc(part))
    return "".join(chunks)


def rich(text, size=26, color=INK, weight=NORMAL, spacing=0.82):
    return MarkupText(
        _markup(text),
        font=SANS,
        font_size=size,
        color=color,
        weight=weight,
        line_spacing=spacing,
    )


_CW = {}
_PROBE = "Вычисление как подстановка: функция x => x, и ещё немного текста."


def _char_w(size):
    if size not in _CW:
        with quiet():
            _CW[size] = Text(_PROBE, font=SANS, font_size=size).width / len(_PROBE)
    return _CW[size]


def wrap(text, size, width, limit=None):
    # backtick spans never break; open *gold* spans are closed and reopened across lines
    text = re.sub(r"`[^`]+`", lambda m: m.group(0).replace(" ", "\u00a0"), text)
    if limit is None:
        limit = max(8, int(width / _char_w(size)))
    lines, cur = [], ""
    for word in text.split(" "):
        visible = len((cur + " " + word).replace("*", "").replace("`", ""))
        if cur and visible > limit:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}" if cur else word
    if cur:
        lines.append(cur)
    out, carry = [], False
    for line in lines:
        if carry:
            line = "*" + line
        carry = line.count("*") % 2 == 1
        out.append(line + ("*" if carry else ""))
    return [line.replace("\u00a0", " ") for line in out]


def line(text, size=26, color=INK, weight=NORMAL):
    # trailing invisible "|" gives every line the same ascent and descent
    mob = rich(text + "|", size, color, weight)
    mob[-1].set_opacity(0)
    return mob


def _para(lines, size, color, weight, center):
    rows = VGroup(*[line(text, size, color, weight) for text in lines])
    return rows.arrange(DOWN, buff=size * 0.0042, aligned_edge=ORIGIN if center else LEFT)


def para(text, size=26, width=6.0, color=INK, weight=NORMAL, center=False):
    if not text.strip():
        return VectorizedPoint()
    limit = max(8, int(width / _char_w(size)))
    while True:
        lines = wrap(text, size, width, limit)
        with quiet():
            mob = _para(lines, size, color, weight, center)
        if mob.width <= width or limit <= 8:
            break
        limit -= 2
    return fit(_para(lines, size, color, weight, center), width)


def bullets(items, size=26, width=6.0, gap=0.26, mark=GOLD, color=INK):
    with quiet():
        cap = Text("Н", font=SANS, font_size=size).height
    rows = VGroup()
    for item in items:
        body = para(item, size, width - 0.42, color)
        dot = Square(side_length=cap * 0.42, stroke_width=0, fill_color=mark, fill_opacity=1)
        dot.rotate(PI / 4)
        dot.next_to(body, LEFT, buff=0.24)
        dot.set_y(body[0].get_center()[1] + cap * 0.08)
        rows.add(VGroup(dot, body))
    return rows.arrange(DOWN, buff=gap, aligned_edge=LEFT)


def callout(text, color=MINT, size=26, width=11.0):
    body = para(text, size, width - 0.6, INK)
    bar = Rectangle(width=0.07, height=body.height + 0.16, stroke_width=0, fill_color=color, fill_opacity=1)
    row = VGroup(bar, body).arrange(RIGHT, buff=0.26)
    frame = RoundedRectangle(
        width=row.width + 0.56,
        height=row.height + 0.36,
        corner_radius=0.1,
        stroke_width=0,
        fill_color=color,
        fill_opacity=0.1,
    )
    frame.move_to(row)
    return VGroup(frame, row)


def quote(text, who, size=30, width=10.5):
    body = para(f"«{text}»", size, width, INK)
    sign = Text(f"— {who}", font=SANS, font_size=size - 8, color=MUTED)
    sign.next_to(body, DOWN, buff=0.22, aligned_edge=RIGHT)
    return VGroup(body, sign)


def tiles(specs, w, size=21, pad=0.26):
    contents = []
    inner = w - 2 * pad - 0.18
    for spec in specs:
        accent = spec.get("accent", GOLD)
        parts = []
        if spec.get("head") is not None:
            parts.append(fit(spec["head"], inner))
        title = Text(spec["title"], font=SANS, font_size=size + 5, color=INK, weight=BOLD)
        fit(title, inner)
        parts.append(title)
        if spec.get("tag"):
            parts.append(fit(Text(spec["tag"], font=SANS, font_size=size - 3, color=accent, weight=BOLD), inner))
        if spec.get("body"):
            parts.append(para(spec["body"], size, inner, MUTED))
        contents.append(VGroup(*parts).arrange(DOWN, buff=0.14, aligned_edge=LEFT))
    h = max(c.height for c in contents) + 2 * pad
    out = VGroup()
    for spec, body in zip(specs, contents):
        frame = RoundedRectangle(
            width=w,
            height=h,
            corner_radius=0.12,
            stroke_color=LINE,
            stroke_width=1.4,
            fill_color=CARD,
            fill_opacity=1,
        )
        bar = Rectangle(
            width=0.06,
            height=h - 2 * pad,
            stroke_width=0,
            fill_color=spec.get("accent", GOLD),
            fill_opacity=1,
        )
        bar.move_to(frame.get_left() + RIGHT * (pad * 0.6))
        body.next_to(frame.get_corner(UL), DR, buff=0)
        body.shift(RIGHT * (pad + 0.14) + DOWN * pad)
        out.add(VGroup(frame, bar, body))
    return out


def timeline(events, width=12.4, size=19):
    step = width / len(events)
    line = Line(LEFT * width / 2, RIGHT * width / 2, color=LINE, stroke_width=2)
    items = VGroup()
    for i, (year, label, color) in enumerate(events):
        x = -width / 2 + step * (i + 0.5)
        dot = Dot([x, 0, 0], radius=0.075, color=color)
        yr = Text(year, font=SANS, font_size=size + 5, color=color, weight=BOLD)
        yr.next_to(dot, UP, buff=0.18)
        lab = para(label, size, step - 0.12, INK, center=True)
        lab.next_to(dot, DOWN, buff=0.22)
        items.add(VGroup(dot, yr, lab))
    return VGroup(line, items)


def table(rows, widths, size=21, gap=0.2):
    out = VGroup()
    total = sum(widths)
    for r, row in enumerate(rows):
        cells = VGroup()
        x = 0
        for c, (text, w) in enumerate(zip(row, widths)):
            if r == 0:
                cell = para(text, size, w - 0.25, GOLD, weight=BOLD)
            else:
                cell = para(text, size, w - 0.25, MUTED if c == 0 else INK)
            cell.move_to([x + cell.width / 2, 0, 0])
            cell.align_to(ORIGIN, UP)
            cells.add(cell)
            x += w
        out.add(cells)
    out.arrange(DOWN, buff=gap * 2, aligned_edge=LEFT)
    for r, cells in enumerate(out):
        x = out.get_left()[0]
        for cell, w in zip(cells, widths):
            cell.set_x(x + cell.width / 2)
            x += w
    rules = VGroup()
    for r in range(1, len(out)):
        y = (out[r - 1].get_bottom()[1] + out[r].get_top()[1]) / 2
        left = out.get_left()[0]
        rule = Line([left, y, 0], [left + total - 0.2, y, 0], color=LINE, stroke_width=1.2)
        rules.add(rule)
        out[r].add(rule)
    return out


def note(text, size=18):
    return Text(text, font=SANS, font_size=size, color=MUTED)


def serif(text, size=40, color=INK):
    return Text(text, font=SERIF, font_size=size, color=color)


def panel(mob, pad_x=0.32, pad_y=0.24, fill=CARD):
    frame = RoundedRectangle(
        width=mob.width + pad_x * 2,
        height=mob.height + pad_y * 2,
        corner_radius=0.1,
        stroke_color=LINE,
        stroke_width=1.4,
        fill_color=fill,
        fill_opacity=1,
    )
    frame.move_to(mob)
    return VGroup(frame, mob)


def highlight(src, lang):
    # ⟦…⟧ marks the fragment that changed: it is painted mint whole
    out = []
    for i, seg in enumerate(re.split("[⟦⟧]", src)):
        if i % 2:
            out.append(f'<span fgcolor="{MINT}">{esc(seg)}</span>')
        else:
            out.append(_paint(seg, lang))
    return "".join(out)


def _paint(src, lang):
    keys = _KW[lang]
    out = []
    for match in _TOKEN.finditer(src):
        tok = match.group(0)
        if tok.startswith("//") or tok.startswith("--"):
            color = DIM
        elif tok.startswith(("'", '"')):
            color = CORAL
        elif tok.isdigit():
            color = SKY
        elif tok in keys:
            color = GOLD
        elif tok in _TY:
            color = SKY
        elif tok in {"=>", "->", "\\", "λ"}:
            color = GOLD
        else:
            color = INK
        out.append(f'<span fgcolor="{color}">{esc(tok)}</span>')
    return "".join(out)


def code_card(src, lang, size=20):
    body = MarkupText(
        highlight(src, lang),
        font=MONO,
        font_size=size,
        line_spacing=0.7,
    )
    return panel(body, pad_x=0.34, pad_y=0.26)


def formula(parts, size=42, gap=0.1):
    mobs = []
    for part in parts:
        text, color, key = part
        tok = Text(text, font=SERIF, font_size=size, color=color)
        tok.key = key
        tok.src = text
        tok.fs = size
        mobs.append(tok)
    group = VGroup(*mobs).arrange(RIGHT, buff=gap)
    return settle(group)


def settle(group):
    # arrange centers every token, so the λ dot would float at mid-height like a "·"
    for tok in group:
        if getattr(tok, "src", None) == ".":
            with quiet():
                ref = Text("x", font=SERIF, font_size=tok.fs)
            base = tok.get_center()[1] - ref.height / 2
            tok.shift(UP * (base - tok.get_bottom()[1]))
    return group


def by_key(group, key):
    return [m for m in group if getattr(m, "key", None) == key]


def fly_subst(scene, group, hole, arg, drop, run_time=1.05):
    holes = by_key(group, hole)
    arg_m = by_key(group, arg)[0]
    gone = set(holes)
    gone.add(arg_m)
    for key in drop:
        gone.update(by_key(group, key))
    copies = []
    anims = []
    for hole_m in holes:
        copy = arg_m.copy()
        copy.key = "kept"
        copies.append(copy)
        scene.add(copy)
        anims.append(copy.animate.move_to(hole_m))
        anims.append(hole_m.animate.set_opacity(0))
    for mob in gone:
        if mob not in holes:
            anims.append(mob.animate.set_opacity(0))
    scene.play(*anims, run_time=run_time)
    placed = dict(zip(holes, copies))
    kept = []
    for mob in group:
        if mob in placed:
            kept.append(placed[mob])
        elif mob not in gone:
            kept.append(mob)
    ghost = settle(VGroup(*[m.copy() for m in kept]).arrange(RIGHT, buff=0.06))
    ghost.move_to(group)
    scene.play(
        *[mob.animate.move_to(target) for mob, target in zip(kept, ghost)],
        run_time=0.55,
    )
    return VGroup(*kept)


def halo(mob, color=CORAL):
    return SurroundingRectangle(
        mob,
        color=color,
        buff=0.14,
        corner_radius=0.08,
        stroke_width=1.8,
    )


def chip(label, sub, accent=GOLD):
    title = Text(label, font=SANS, font_size=26, color=INK, weight=BOLD)
    body = Text(sub, font=SANS, font_size=20, color=MUTED)
    text = VGroup(title, body).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    mark = Rectangle(width=0.06, height=text.height, stroke_width=0, fill_color=accent, fill_opacity=1)
    row = VGroup(mark, text).arrange(RIGHT, buff=0.2, aligned_edge=UP)
    return panel(row, pad_x=0.28, pad_y=0.22)


def church_stack(n, caption):
    x = panel(Text("x", font=SERIF, font_size=28, color=SKY), pad_x=0.22, pad_y=0.14)
    layers = []
    for _ in range(n):
        layers.append(panel(Text("f", font=SERIF, font_size=28, color=GOLD), pad_x=0.22, pad_y=0.14))
    stack = VGroup(*layers, x).arrange(DOWN, buff=0.1)
    cap = Text(caption, font=SANS, font_size=18, color=MUTED)
    cap.next_to(stack, DOWN, buff=0.16)
    return VGroup(stack, cap)


def tape(symbols, head_at):
    cells = VGroup()
    labels = []
    for symbol in symbols:
        box = Rectangle(
            width=0.82,
            height=0.82,
            stroke_color=LINE,
            stroke_width=1.5,
            fill_color=CARD,
            fill_opacity=1,
        )
        lab = Text(symbol, font=MONO, font_size=26, color=INK)
        lab.move_to(box)
        labels.append(lab)
        cells.add(VGroup(box, lab))
    cells.arrange(RIGHT, buff=0)
    head = Triangle(color=GOLD, fill_color=GOLD, fill_opacity=1, stroke_width=0)
    head.stretch_to_fit_height(0.2)
    head.stretch_to_fit_width(0.24)
    head.rotate(PI)
    head.next_to(cells[head_at], UP, buff=0.1)
    state = Text("q1", font=MONO, font_size=18, color=GOLD)
    state.next_to(head, UP, buff=0.08)
    return VGroup(cells, head, state), cells, labels, head


def tree_node(label, color=INK):
    text = Text(label, font=SERIF, font_size=28, color=color)
    box = RoundedRectangle(
        width=max(0.78, text.width + 0.32),
        height=text.height + 0.28,
        corner_radius=0.08,
        stroke_color=LINE,
        stroke_width=1.4,
        fill_color=CARD,
        fill_opacity=1,
    )
    text.move_to(box)
    return VGroup(box, text)


def edge(a, b):
    return Line(
        a.get_bottom(),
        b.get_top(),
        stroke_width=1.4,
        color=DIM,
    )
