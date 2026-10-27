from manim import *
from manim._config.utils import ManimConfig
from manim_slides import Slide

# manim 0.22 dropped write_to_movie; manim-slides 5.7 still sets it
if not hasattr(ManimConfig, "write_to_movie"):

    def _ignore_write_to_movie(self, value):
        return None

    ManimConfig.write_to_movie = property(lambda self: True, _ignore_write_to_movie)

BG = "#1C1C1C"
INK = "#F4F4F4"
MUTED = "#9C9C9C"
GOLD = "#F6C445"
SKY = "#58C4DD"
CORAL = "#FF6B6B"
MINT = "#83C167"
CARD = "#2A2A2A"
LINE = "#3F3F3F"
DIM = "#7A7A7A"

SANS = "Noto Sans"
SERIF = "Linux Libertine O"
MONO = "iA Writer Mono S"

config.background_color = BG

PARTS = ["история", "язык", "данные", "рекурсия", "типы", "практика"]

# while > 0, created mobjects are not counted by Talk._balance
QUIET = [0]


class quiet:
    def __enter__(self):
        QUIET[0] += 1

    def __exit__(self, *exc):
        QUIET[0] -= 1


def fit(mob, max_w=12.5):
    if mob.width > max_w:
        mob.scale(max_w / mob.width)
    return mob


class Talk(Slide):
    skip_reversing = True
    part = ""
    title = ""
    idx = 1
    total = 1

    def construct(self):
        from lc.notes import NOTES

        self.wait_time_between_slides = 0.12
        self._extra = NOTES.get(type(self).__name__, {})
        self._briefed = False
        self._chrome()
        self._balanced = False
        self._placed = []
        self._patched = []
        self._patch()
        try:
            self.draw()
        finally:
            self._unpatch()
            self._balance()
        tail = self._tail()
        if tail:
            self._base_slide_config.notes += tail

    def _tail(self):
        parts = []
        if self._extra.get("qa"):
            lines = [f"- *{q}* — {a}" for q, a in self._extra["qa"]]
            parts.append("**Если спросят**\n\n" + "\n".join(lines))
        if self._extra.get("bridge"):
            parts.append(f"**Переход:** {self._extra['bridge']}")
        return "".join(f"\n\n{p}" for p in parts)

    def next_slide(self, *args, **kwargs):
        self._balance()
        if not self._briefed and kwargs.get("notes"):
            self._briefed = True
            brief = self._extra.get("brief")
            if brief:
                kwargs["notes"] += f"\n\n**Контекст:** {brief}"
        return super().next_slide(*args, **kwargs)

    def play(self, *args, **kwargs):
        self._balance()
        return super().play(*args, **kwargs)

    def _chrome(self):
        kick = Text(self.part, font=SANS, font_size=22, color=GOLD, weight=BOLD)
        kick.to_corner(UL, buff=0.42)
        title = Text(self.title, font=SANS, font_size=42, color=INK, weight=BOLD)
        fit(title, 12.4)
        title.next_to(kick, DOWN, buff=0.16, aligned_edge=LEFT)
        self.add(kick, title)
        self.anchor = title
        self._title_bottom = title.get_bottom()[1]
        self._footer()

    def _footer(self):
        marks = [
            Text(
                name,
                font=SANS,
                font_size=16,
                color=GOLD if name == self.part else DIM,
                weight=BOLD if name == self.part else NORMAL,
            )
            for name in PARTS
        ]
        track = VGroup(*marks).arrange(RIGHT, buff=0.34)
        track.to_corner(DL, buff=0.3)
        page = Text(f"{self.idx} / {self.total}", font=MONO, font_size=16, color=DIM)
        page.to_corner(DR, buff=0.3)
        page.align_to(track, DOWN)
        half = config.frame_width / 2
        y = -config.frame_height / 2 + 0.03
        rail = Line([-half, y, 0], [half, y, 0], color=LINE, stroke_width=3)
        done = Line([-half, y, 0], [-half + 2 * half * self.idx / self.total, y, 0], color=GOLD, stroke_width=3)
        self.add(track, page, rail, done)

    def _note(self, mob):
        if not self._balanced and not QUIET[0]:
            self._placed.append(mob)

    def _patch(self):
        talk = self

        def wrap(fn):
            def wrapped(mob, *args, **kwargs):
                out = fn(mob, *args, **kwargs)
                talk._note(mob)
                return out

            return wrapped

        for cls, names in (
            (Mobject, ("next_to", "move_to", "shift", "set_x", "set_y", "align_to", "scale", "arrange", "center", "to_edge", "to_corner")),
            (VMobject, ("set_points_as_corners",)),
        ):
            for name in names:
                fn = getattr(cls, name)
                self._patched.append((cls, name, fn))
                setattr(cls, name, wrap(fn))

    def _unpatch(self):
        for cls, name, fn in self._patched:
            setattr(cls, name, fn)
        self._patched = []

    def _roots(self):
        # groups may share children, so each leaf is claimed once, biggest group first
        unique = list({id(m): m for m in self._placed}.values())
        unique.sort(key=lambda m: len(m.get_family()), reverse=True)
        claimed = set()
        roots = []
        for mob in unique:
            family = mob.get_family()
            if any(id(sub) in claimed for sub in family):
                continue
            if mob.width == 0 and mob.height == 0:
                continue
            claimed.update(id(sub) for sub in family)
            roots.append(mob)
        return roots

    def _balance(self):
        if self._balanced:
            return
        self._balanced = True
        self._unpatch()
        roots = self._roots()
        if not roots:
            return
        top = max(mob.get_top()[1] for mob in roots)
        bottom = min(mob.get_bottom()[1] for mob in roots)
        height = top - bottom
        if height < 0.05:
            return
        top_limit = self._title_bottom - 0.36
        bottom_limit = -3.2
        band = top_limit - bottom_limit
        if height > band:
            left = min(mob.get_left()[0] for mob in roots)
            right = max(mob.get_right()[0] for mob in roots)
            center = np.array([(left + right) / 2, (top + bottom) / 2, 0])
            factor = band / height
            for mob in roots:
                mob.scale(factor, about_point=center)
            top = max(mob.get_top()[1] for mob in roots)
            bottom = min(mob.get_bottom()[1] for mob in roots)
        dy = (top_limit + bottom_limit) / 2 - (top + bottom) / 2
        for mob in roots:
            mob.shift(UP * dy)

    def put(self, mob, buff=0.32, max_w=12.2):
        fit(mob, max_w)
        mob.next_to(self.anchor, DOWN, buff=buff, aligned_edge=LEFT)
        self.anchor = mob
        return mob

    def stage(self, mob, buff=0.45, max_w=12.0):
        fit(mob, max_w)
        mob.next_to(self.anchor, DOWN, buff=buff)
        mob.set_x(0)
        self.anchor = mob
        return mob

    def say(self, text, size=30, buff=0.38):
        from lc.widgets import rich

        mob = rich(text, size=size)
        fit(mob, 12.2)
        mob.next_to(self.anchor, DOWN, buff=buff)
        mob.set_x(0)
        self.anchor = mob
        return mob

    def split(self, left, right, ratio=0.5, gap=0.7, buff=0.5, width=12.6):
        lw = (width - gap) * ratio
        rw = width - gap - lw
        fit(left, lw)
        fit(right, rw)
        x0 = -width / 2
        top = self.anchor.get_bottom()[1] - buff
        cy = top - max(left.height, right.height) / 2
        left.move_to([x0 + lw / 2, cy, 0])
        right.move_to([0, cy, 0])
        right.set_x(x0 + lw + gap + right.width / 2)
        self.anchor = VGroup(left, right)
        return left, right

    def points(self, items, size=26, width=12.0, buff=0.5, **kw):
        from lc.widgets import bullets

        mob = bullets(items, size=size, width=width, **kw)
        return self.stage(mob, buff=buff, max_w=width)

    def gist(self, text, size=28):
        from lc.widgets import callout

        mob = self.stage(callout(text, color=GOLD, size=size, width=12.0), buff=0.36)
        self.add(mob)
        return mob

    def punch(self, text, color=MINT, size=26, buff=0.45):
        from lc.widgets import callout

        return self.stage(callout(text, color=color, size=size), buff=buff)

    def beat(self, notes, *anims, run_time=0.65):
        self.next_slide(notes=notes)
        if anims:
            self.play(*anims, run_time=run_time)

    def draw(self):
        raise NotImplementedError
