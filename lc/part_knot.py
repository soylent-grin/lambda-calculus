from lc.registry import slide
from lc.theme import *
from lc.widgets import *


@slide
class S20_NoNames(Talk):
    part = "рекурсия"
    title = "Рекурсия без имени?"

    def draw(self):
        self.gist("Рекурсия обычно держится на *имени*: функция вызывает себя по имени. В λ имён нет")
        line = VGroup(
            serif("λn. ", 44),
            serif("n = 0", 44, MUTED),
            serif("  ?  1  :  n × ", 44),
            serif("fact", 48, CORAL),
            serif("(n − 1)", 44),
        ).arrange(RIGHT, buff=0.08)
        self.stage(line, buff=0.6)
        strike = Line(
            line[3].get_corner(DL) + DOWN * 0.05,
            line[3].get_corner(UR) + UP * 0.05,
            color=CORAL,
            stroke_width=5,
        )
        pts = self.points(
            [
                "В λ все функции анонимны: нет `function fact`, нет глобальной области",
                "Подстановка умеет только заполнять параметры. Откуда взяться повторению?",
            ],
            size=25,
            width=11.6,
        )
        p = self.punch("Ключ — старая математическая идея: *неподвижная точка*")
        self.beat("Факториал должен позвать себя. Но кого звать?", FadeIn(line))
        self.next_slide(notes="Зачеркнуть именно вызов. Связать fact нечем: имени нет, есть только лямбда.")
        self.play(Create(strike), run_time=0.45)
        for row, n in zip(
            pts,
            [
                "В каждом языке имя функции видно внутри её тела. Это особое правило. В λ его нет — и добавлять не хотим.",
                "Вспомните Ω: самоприменение уже дало бесконечное повторение. Нужно его приручить.",
            ],
        ):
            self.beat(n, FadeIn(row, shift=RIGHT * 0.08))
        self.beat("Решение придёт из математики, а не из программирования. Начнём с графика косинуса.", FadeIn(p))


@slide
class S21_FixMath(Talk):
    part = "рекурсия"
    title = "Неподвижная точка: сначала математика"

    def draw(self):
        self.gist("*Неподвижная точка* функции f — такое x, что f(x) = x: функция его «не сдвигает»")
        axes = Axes(
            x_range=[0, 1.6, 0.4],
            y_range=[0, 1.6, 0.4],
            x_length=4.4,
            y_length=4.4,
            tips=False,
            axis_config=dict(color=DIM, stroke_width=2),
        )
        diag = axes.plot(lambda x: x, x_range=[0, 1.6], color=MUTED, stroke_width=2)
        curve = axes.plot(np.cos, x_range=[0, 1.6], color=GOLD, stroke_width=4)
        diag_label = Text("y = x", font=SANS, font_size=18, color=MUTED).next_to(axes.c2p(1.6, 1.6), DOWN, buff=0.1)
        curve_label = Text("y = cos x", font=SANS, font_size=18, color=GOLD).next_to(axes.c2p(0.05, 1.0), UR, buff=0.08)
        segs = []
        x = 0.0
        prev = axes.c2p(x, 0)
        for _ in range(9):
            y = float(np.cos(x))
            up = axes.c2p(x, y)
            side = axes.c2p(y, y)
            segs.append(Line(prev, up, color=SKY, stroke_width=2.5))
            segs.append(Line(up, side, color=SKY, stroke_width=2.5))
            prev = side
            x = y
        web = VGroup(*segs)
        star = Dot(axes.c2p(0.739, 0.739), radius=0.08, color=MINT)
        drop = DashedLine(axes.c2p(0.739, 0.739), axes.c2p(0.739, 0), color=MINT, stroke_width=2)
        star_label = Text("0.739", font=MONO, font_size=20, color=MINT).next_to(axes.c2p(0.739, 0), DOWN, buff=0.12)
        seq = Text("0 → 1 → 0.54 → 0.86 → 0.65 → … → 0.739", font=MONO, font_size=20, color=SKY)
        plot = VGroup(axes, diag, curve, diag_label, curve_label, web, star, drop, star_label)
        left = VGroup(plot, seq).arrange(DOWN, buff=0.3)
        pts = bullets(
            [
                "На графике — пересечение с диагональю y = x. У cos x это 0.739",
                "Найти её можно повторением: x, f(x), f(f(x)), … Жмите cos на калькуляторе — придёте к 0.739",
                "Уравнение x = f(x) определяет x *через самого себя* — как рекурсивное определение",
            ],
            size=25,
            width=6.8,
        )
        self.split(left, pts, ratio=0.42)
        self.beat(
            "Начнём со школьной математики. Неподвижная точка — где график функции пересекает диагональ y = x.",
            Create(axes),
            Create(diag),
            FadeIn(diag_label),
            FadeIn(pts[0]),
        )
        self.beat(
            "Примеры, которые можно проверить в уме: у x² две неподвижные точки, 0 и 1, у x + 1 — ни одной.",
            Create(curve),
            FadeIn(curve_label),
        )
        self.next_slide(notes="«Лесенка»: от x идём вверх до графика — это cos x, потом вбок до диагонали — это делает cos x новым x. Ступеньки сходятся к пересечению.")
        self.play(LaggedStart(*[Create(s) for s in segs], lag_ratio=0.6), FadeIn(seq), FadeIn(pts[1]), run_time=3.0)
        self.play(FadeIn(star, scale=1.6), Create(drop), FadeIn(star_label), run_time=0.5)
        self.beat(
            "Самое важное: x = cos x — это определение x через самого себя. Решить такое уравнение — значит найти неподвижную точку. Дальше мы сделаем то же самое, только x будет функцией.",
            FadeIn(pts[2]),
        )


@slide
class S22_Improve(Talk):
    part = "рекурсия"
    title = "Рекурсия — тоже неподвижная точка"

    def draw(self):
        self.gist("Рекурсивная функция — неподвижная точка «улучшателя» F: *fact = F(fact)*")
        card = code_card("const F = f => n =>\n  n === 0 ? 1 : n * f(n - 1)", "js", size=22)
        rows = [
            ("f₀ = ⊥", ["?", "?", "?", "?", "?"]),
            ("f₁ = F(f₀)", ["1", "?", "?", "?", "?"]),
            ("f₂ = F(f₁)", ["1", "1", "?", "?", "?"]),
            ("f₃ = F(f₂)", ["1", "1", "2", "?", "?"]),
            ("fact = F(fact)", ["1", "1", "2", "6", "24"]),
        ]
        label_w, cell_w, row_h = 2.6, 0.72, 0.46
        head = VGroup(Text("n =", font=MONO, font_size=20, color=MUTED).move_to([label_w - 0.5, 0, 0]))
        for c in range(5):
            head.add(Text(str(c), font=MONO, font_size=20, color=MUTED).move_to([label_w + cell_w * (c + 0.5), 0, 0]))
        grid = VGroup(head)
        for r, (name, vals) in enumerate(rows):
            y = -(r + 1) * row_h
            last = r == len(rows) - 1
            row = VGroup(Text(name, font=SERIF, font_size=24, color=MINT if last else INK).move_to([0, y, 0], aligned_edge=LEFT))
            row[0].set_x(row[0].width / 2)
            for c, v in enumerate(vals):
                learned = r > 0 and v != "?" and rows[r - 1][1][c] == "?"
                color = DIM if v == "?" else (GOLD if learned else INK)
                row.add(Text(v, font=MONO, font_size=22, color=color).move_to([label_w + cell_w * (c + 0.5), y, 0]))
            grid.add(row)
        left = VGroup(card, grid).arrange(DOWN, buff=0.45)
        pts = bullets(
            [
                "F не рекурсивна: она получает *старую* версию функции и строит улучшенную",
                "Начинаем с функции, которая не знает ничего (⊥). Каждое применение F добавляет один ответ",
                "Предел — функция, которую F уже не меняет. Это и есть факториал",
            ],
            size=25,
            width=6.4,
        )
        self.split(left, pts, ratio=0.48)
        self.beat(
            "F выглядит как факториал, но вместо вызова себя вызывает параметр f. Это «улучшатель»: дай ему приближение — получишь приближение получше.",
            FadeIn(card),
            FadeIn(grid[0]),
            FadeIn(pts[0]),
        )
        self.beat("Стартуем с функции, которая не знает ни одного ответа: на любой вызов зависает. Знак ⊥ — «дно».", FadeIn(grid[1]), FadeIn(pts[1]))
        self.beat(
            "f₁ знает ответ для 0: там F не обращается к f. Для остальных n зовёт f₀ и зависает.",
            FadeIn(grid[2], shift=DOWN * 0.05),
        )
        self.beat(
            "f₂ = F(f₁): для n = 1 зовёт f₁(0), а его ответ уже известен. Золотым — новое выученное значение.",
            FadeIn(grid[3], shift=DOWN * 0.05),
        )
        self.beat("Каждый следующий шаг — ещё один ответ. Это та же «лесенка», что у косинуса, только по функциям.", FadeIn(grid[4], shift=DOWN * 0.05))
        self.beat(
            "В пределе — функция, которая знает все ответы, и F её уже не улучшает. Теорема Клини: такая точка всегда есть. Осталось получить её без имён.",
            FadeIn(grid[5], shift=DOWN * 0.05),
            FadeIn(pts[2]),
        )


@slide
class S23_Self(Talk):
    part = "рекурсия"
    title = "Трюк: передай себя сам"

    def draw(self):
        self.gist("В *теле* λ нет имени функции — рекурсия через параметр *self*, а не через `fact` внутри себя")
        card = code_card(
            "const half = self => n =>\n"
            "  n === 0 ? 1 : n * self(self)(n - 1)\n"
            "\n"
            "half(half)(5)  // 120",
            "js",
            size=22,
        )
        term = formula(
            [
                ("(", INK, "lp"),
                ("λ", GOLD, "lam"),
                ("x", GOLD, "p"),
                (".", INK, "d"),
                ("x", SKY, "hole"),
                ("x", SKY, "hole"),
                (")", INK, "rp"),
                ("half", CORAL, "arg"),
            ],
            size=40,
        )
        slot = Rectangle(width=4.0, height=0.9, stroke_width=0, fill_opacity=0)
        cap = note("«примени к себе»: тот же x x, что у Рассела и в Ω", 20)
        left = VGroup(card, slot, cap).arrange(DOWN, buff=0.4)
        pts = bullets(
            [
                "Внутри — только `self`, не `half`: тело *не ссылается* на имя снаружи",
                "`half` в JS — ярлык для «примени эту же функцию к себе»; в λ это `(λ…)(λ…)`",
                "`half(half)` — один стартовый вызов; дальше рекурсия идёт через `self(self)`",
            ],
            size=25,
            width=6.4,
        )
        self.split(left, pts, ratio=0.5)
        term.move_to(slot)
        self.beat(
            "Отличие от `function fact`: внутри нельзя написать `fact(n−1)` — в λ нет такого имени. Зато можно принять «себя» параметром.",
            FadeIn(card),
        )
        self.beat("Рекурсивный вызов — `self(self)(n−1)`, не `half(…)`. Переименуйте `half` в `foo` — тело менять не нужно.", FadeIn(pts[0]))
        self.beat("`half(half)` — не «рекурсия по имени half», а один раз передали функцию самой себе как аргумент.", FadeIn(pts[1]), FadeIn(term))
        self.next_slide(notes="В λ-записи «примени к себе» — это λx. x x. Подставляем half на оба места x.")
        fly_subst(self, term, "hole", "arg", ["lp", "lam", "p", "d", "rp"])
        self.beat(
            "Тот же x x, что в парадоксе Рассела и в Ω. Здесь самоприменение не ломает систему, а работает на нас.",
            FadeIn(cap),
        )
        self.beat("Хочется писать обычный F с f(n − 1), а самоприменение спрятать в отдельную машинку. Её и выведем.", FadeIn(pts[2]))


def paint(text, size=30, font=SERIF, colors=None):
    colors = colors or {"F": GOLD, "g": SKY}
    body = "".join(f'<span fgcolor="{colors[ch]}">{ch}</span>' if ch in colors else esc(ch) for ch in text)
    return MarkupText(body, font=font, font_size=size, color=INK)


@slide
class S24_Y(Talk):
    part = "рекурсия"
    title = "От half к Y за три шага"

    def draw(self):
        self.gist("Отделяем трюк `self(self)` от логики задачи — трюк и есть *Y*, логика — это *F*")
        steps = [
            (
                "const half = self => n =>\n"
                "  n === 0 ? 1 : n * ⟦self(self)⟧(n - 1)",
                "self(self) играет роль fact",
            ),
            (
                "const half = self => ⟦F⟧(self(self))\n"
                "const fact = half(half)",
                "остальное — это F, улучшатель из таблицы",
            ),
            (
                "const Y = ⟦F =>⟧\n"
                "  (⟦x => F(x(x))⟧)(⟦x => F(x(x))⟧)",
                "F — параметр, half подставили на место имени",
            ),
        ]
        rows = VGroup()
        for i, (src, cap) in enumerate(steps, 1):
            badge = Text(str(i), font=SANS, font_size=26, color=GOLD, weight=BOLD)
            body = VGroup(note(cap, 18), code_card(src, "js", size=20)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            rows.add(VGroup(badge, body).arrange(RIGHT, buff=0.24, aligned_edge=UP))
        rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        lam = serif("Y  =  λF. (λx. F (x x)) (λx. F (x x))", 26, MINT)
        left = VGroup(rows, lam).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        pts = bullets(
            [
                "Каждый шаг меняет *одну* вещь — она зелёная",
                "Тело half — это F, где на месте f стоит `self(self)`",
                "Y не знает о задаче: `Y(Ffib)` — уже Фибоначчи",
                "`x => F(x(x))` — это half с именем x вместо self",
            ],
            size=24,
            width=5.6,
        )
        self.split(left, pts, ratio=0.56)
        self.beat(
            "Вернёмся к half. Зелёным — self(self): вызов self(self)(n − 1) считает факториал от n − 1, то есть играет роль fact.",
            FadeIn(rows[0]),
            FadeIn(pts[0]),
        )
        self.beat(
            "Всё, кроме self(self), — это F из слайда про улучшатель. Значит, half = F, которому вместо f передали self(self).",
            FadeIn(rows[1], shift=UP * 0.05),
            FadeIn(pts[1]),
        )
        self.beat(
            "Сделаем F параметром и подставим half по месту вместо имени. Две одинаковые половинки x => F(x(x)) — это Y. F может быть любым.",
            FadeIn(rows[2], shift=UP * 0.05),
            FadeIn(pts[2]),
        )
        self.beat("То же в λ-нотации. Это Y-комбинатор Карри. Дальше — почему он работает.", FadeIn(lam), FadeIn(pts[3]))


@slide
class S25_Tower(Talk):
    part = "рекурсия"
    title = "Почему Y работает: башня из F"

    def draw(self):
        self.gist("*Y F* разворачивается в *F(F(F(…)))* — та же лесенка, что у косинуса, только по функциям")
        gdef = panel(paint("g  =  λx. F (x x)", 30), pad_x=0.3, pad_y=0.18)
        gcap = note("половинка Y; тогда Y F = g g", 18)
        head = VGroup(gdef, gcap).arrange(RIGHT, buff=0.3)
        exprs = [
            ("Y F  =  g g", "по определению Y"),
            ("=  F (g g)", "x := g"),
            ("=  F (F (g g))", "ещё раз"),
            ("=  F (F (F ( … )))", "сколько понадобится"),
        ]
        rows = VGroup(*[paint(e, 32) for e, _ in exprs]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        rows[1:].shift(RIGHT * (rows[0][:4].width + 0.12))
        whys = VGroup()
        for row, (_, why) in zip(rows, exprs):
            w = note(why, 18)
            w.move_to([rows.get_right()[0] + 0.5 + w.width / 2, row.get_center()[1], 0])
            whys.add(w)
        left = VGroup(head, VGroup(rows, whys)).arrange(DOWN, buff=0.5, aligned_edge=LEFT)

        cos_row = VGroup(
            serif("cos(cos(cos(… 0)))", 26, INK),
            serif("→  0.739", 26, MINT),
        ).arrange(RIGHT, buff=0.24)
        f_row = VGroup(
            paint("F(F(F(… ⊥)))", 26),
            serif("→  fact", 26, MINT),
        ).arrange(RIGHT, buff=0.24)
        cmp = VGroup(
            VGroup(note("числа: жмём cos", 18), cos_row).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
            VGroup(note("функции: строки f₀, f₁, f₂ … из таблицы", 18), f_row).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
        ).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        right = panel(cmp, pad_x=0.36, pad_y=0.3)
        self.split(left, right, ratio=0.58)
        p = self.punch("Снимите с бесконечной башни одну F — останется та же башня. Поэтому *Y F = F (Y F)*: это неподвижная точка F")

        self.beat(
            "Дадим имя половинке Y: g берёт x и возвращает F от x x. Тогда Y F — это просто g, применённое к g.",
            FadeIn(head),
            FadeIn(rows[0]),
            FadeIn(whys[0]),
        )
        self.next_slide(notes="Один β-шаг: g применяем к g, на место x подставляем g. Получаем F(g g). Внутри снова g g!")
        self.play(TransformMatchingShapes(rows[0].copy(), rows[1]), FadeIn(whys[1]), run_time=1.0)
        self.next_slide(notes="g g снова превращается в F(g g). Каждый шаг дописывает одну F снаружи.")
        self.play(TransformMatchingShapes(rows[1].copy(), rows[2]), FadeIn(whys[2]), run_time=1.0)
        self.beat("И так без конца: башня F(F(F(…))).", FadeIn(rows[3], shift=DOWN * 0.05), FadeIn(whys[3]))
        self.beat(
            "Сравните с косинусом: жали cos снова и снова — пришли к неподвижной точке 0.739. Тут F применяется снова и снова, как строки таблицы f₀, f₁, f₂. Предел — факториал.",
            FadeIn(right),
        )
        self.beat(
            "Главное: если от бесконечной башни отнять одну F сверху, останется та же башня. Значит, Y F = F(Y F) — это ровно уравнение fact = F(fact).",
            FadeIn(p),
        )


@slide
class S25_Run(Talk):
    part = "рекурсия"
    title = "2! по шагам: башня строится по требованию"

    def draw(self):
        self.gist("Новый этаж F появляется, только когда F зовёт f. При n\u00a0=\u00a00 f не нужен — башня кончается")
        colors = {"Y": SKY, "F": GOLD}
        levels = [
            ("Y(F)(2) → 2 * Y(F)(1)", "= 2"),
            ("Y(F)(1) → 1 * Y(F)(0)", "= 1"),
            ("Y(F)(0) → 1", "= 1"),
        ]
        heads = [paint(h, 26, MONO, colors) for h, _ in levels]
        frames = []
        inner = None
        for i in reversed(range(len(levels))):
            content = heads[i] if inner is None else VGroup(heads[i], inner).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            frame = RoundedRectangle(
                width=content.width + 0.5,
                height=content.height + 0.4,
                corner_radius=0.12,
                stroke_color=SKY,
                stroke_width=2,
                stroke_opacity=1 - 0.25 * i,
                fill_color=SKY,
                fill_opacity=0.05,
            )
            frame.move_to(content)
            frames.insert(0, frame)
            inner = VGroup(frame, content)
        doll = inner
        results = VGroup()
        for head, (_, res) in zip(heads, levels):
            r = Text(res, font=MONO, font_size=26, color=MINT)
            r.move_to([doll.get_right()[0] + 0.35 + r.width / 2, head.get_center()[1], 0])
            results.add(r)
        cap = note("вглубь — пока F просит f, наружу — умножения", 18)
        left = VGroup(VGroup(doll, results), cap).arrange(DOWN, buff=0.3)

        head = Text("В настоящем JS", font=SANS, font_size=22, color=GOLD, weight=BOLD)
        why = para(
            "JS вычисляет аргумент сразу: `x(x)` уйдёт в бесконечность раньше, чем F его позовёт. Обёртка `v => …` откладывает вызов — это *Z*",
            21,
            5.0,
        )
        z = code_card(
            "const Z = F =>\n"
            "  (x => F(⟦v => ⟧x(x)⟦(v)⟧))\n"
            "  (x => F(⟦v => ⟧x(x)⟦(v)⟧))\n"
            "\n"
            "Z(F)(5)  // 120",
            "js",
            size=18,
        )
        right = VGroup(head, why, z).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        self.split(left, right, ratio=0.56, gap=0.55)
        notes = [
            "Хотим 2!. Y подаёт в F рекурсивный вызов f = Y(F). n = 2, не ноль — ветка n * f(n − 1), то есть 2 * Y(F)(1).",
            "Чтобы умножить, нужен Y(F)(1). Только сейчас появляется следующий этаж — ещё одна F.",
            "n = 0: F возвращает 1 и f не зовёт. Новый этаж не нужен — башня обрывается. Поэтому нет зацикливания.",
            "Наружу: внутренний вернул 1, средний 1 * 1 = 1, внешний 2 * 1 = 2. Имя fact ни разу не понадобилось.",
            "Если вставить Y в консоль, он зациклится: JS вычисляет x(x) сразу. Обёртка v => … откладывает вызов — это Z, его можно проверить в браузере.",
        ]
        for i in range(3):
            anims = [Create(frames[i]), FadeIn(heads[i])]
            if i == 0:
                anims.append(FadeIn(cap))
            self.beat(notes[i], *anims)
        self.beat(notes[3], LaggedStart(*[FadeIn(results[i], shift=LEFT * 0.1) for i in reversed(range(3))], lag_ratio=0.5), run_time=1.4)
        self.beat(notes[4], FadeIn(head), FadeIn(why), FadeIn(z))
