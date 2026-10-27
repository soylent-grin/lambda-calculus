from lc.part_history import app
from lc.registry import slide
from lc.theme import *
from lc.widgets import *


@slide
class S10_Rule(Talk):
    part = "язык"
    title = "Функция как правило"

    def draw(self):
        self.gist("Для Чёрча функция — *правило вычисления*, а не таблица готовых ответов")
        pairs = VGroup(
            *[serif(t, 34, MUTED) for t in ("1 ↦ 1", "2 ↦ 4", "3 ↦ 9", "…")]
        ).arrange(DOWN, buff=0.12)
        graph = VGroup(pairs, para("таблица: множество пар «вход — выход»", 21, 3.6, MUTED, center=True))
        graph.arrange(DOWN, buff=0.3)
        rule = VGroup(serif("λx. x × x", 52, GOLD), para("правило: способ получить ответ", 21, 3.6, GOLD, center=True))
        rule.arrange(DOWN, buff=0.3)
        versus = VGroup(graph, Text("vs", font=SANS, font_size=26, color=DIM), rule).arrange(RIGHT, buff=0.6)
        self.stage(versus, buff=0.45)
        pts = self.points(
            [
                "Таблица говорит только, *что* получится. Правило говорит, *как* это получить — так думает программист",
                "Правило — само по себе значение: его можно передать, вернуть и даже применить к самому себе",
            ],
            size=25,
            width=11.6,
        )
        self.beat("Два способа сказать «квадрат». Слева таблица — бесконечная. Справа короткое правило.", FadeIn(graph))
        self.beat("λx. x × x читается «функция от x, которая возвращает x × x». Точка отделяет параметр от тела, это не умножение. В JavaScript — x => x * x.", FadeIn(versus[1]), FadeIn(rule))
        notes = [
            "Математики называют это экстенсиональным и интенсиональным взглядом. Второй — и есть вычисление.",
            "В теории множеств функцию нельзя применить к себе. В λ — можно. Отсюда и сила, и парадоксы.",
        ]
        for row, n in zip(pts, notes):
            self.beat(n, FadeIn(row, shift=RIGHT * 0.08))


@slide
class S11_Syntax(Talk):
    part = "язык"
    title = "Весь язык — три формы"

    def draw(self):
        self.gist("В языке всего три конструкции: *имя*, *функция* и *вызов*. Больше ничего нет")

        def piece(text, color, label, sub):
            term = serif(text, 58, color)
            lab = Text(label, font=SANS, font_size=24, color=INK, weight=BOLD)
            hint = Text(sub, font=MONO, font_size=22, color=MUTED)
            return VGroup(term, lab, hint).arrange(DOWN, buff=0.16)

        items = VGroup(
            piece("x", SKY, "переменная", "x"),
            piece("λx. M", GOLD, "функция", "x => M"),
            piece("M N", INK, "вызов", "M(N)"),
        ).arrange(RIGHT, buff=1.3, aligned_edge=UP)
        self.stage(items, buff=0.5)
        pts = self.points(
            [
                "Аргумент всегда один. Функция двух аргументов — функция, которая возвращает функцию: λx. λy. M (*каррирование*)",
                "Ни чисел, ни if, ни циклов. Всё это будет *определено* через три формы",
            ],
            size=25,
            width=11.6,
        )
        notes = [
            "Переменная — просто имя. Позже на её место что-то подставят.",
            "Абстракция — анонимная функция. Параметр x, тело M.",
            "Применение — вызов. Пробел и есть вызов, как в Haskell; f a b значит (f a) b.",
        ]
        for it, n in zip(items, notes):
            self.beat(n, FadeIn(it, shift=UP * 0.06))
        for row, n in zip(
            pts,
            [
                "Каррирование названо в честь Хаскелла Карри, хотя раньше его описали Шейнфинкель (1924) и Фреге. Отсюда частичное применение.",
                "Как вентиль NAND в электронике: минимальный базис, из которого собирается всё. Через пару разделов отсюда вырастут логика, числа и рекурсия.",
            ],
        ):
            self.beat(n, FadeIn(row, shift=RIGHT * 0.08))


@slide
class S12_Scope(Talk):
    part = "язык"
    title = "Связанные и свободные имена"

    def draw(self):
        self.gist("Параметр *связан* внутри своей функции. Остальные имена *свободны* — они приходят снаружи")
        term = formula(
            [
                ("λ", GOLD, "lam"),
                ("x", GOLD, "p"),
                (".", INK, "d"),
                ("x", SKY, "bx"),
                ("y", CORAL, "fy"),
            ],
            size=64,
            gap=0.16,
        )
        by_key(term, "fy")[0].shift(RIGHT * 0.22)
        bound = VGroup(*by_key(term, "lam"), *by_key(term, "p"), *by_key(term, "d"), *by_key(term, "bx"))
        box = SurroundingRectangle(bound, color=GOLD, buff=0.14, corner_radius=0.08, stroke_width=2)
        legend = VGroup(
            Text("параметр", font=SANS, font_size=22, color=GOLD, weight=BOLD),
            Text("связанное вхождение", font=SANS, font_size=22, color=SKY, weight=BOLD),
            Text("свободное имя", font=SANS, font_size=22, color=CORAL, weight=BOLD),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        left = VGroup(VGroup(term, box), legend).arrange(DOWN, buff=0.5)
        pts = bullets(
            [
                "Связанное имя — как параметр функции. Свободное — как переменная из замыкания",
                "Имя параметра не важно: λx. x и λz. z — одна и та же функция (*α-эквивалентность*)",
                "При подстановке свободное имя не должно случайно стать связанным — иначе изменится смысл",
            ],
            size=25,
            width=7.0,
        )
        self.split(left, pts, ratio=0.38)
        self.beat("Три роли, три цвета. Эти цвета сохранятся до конца лекции.", FadeIn(term), FadeIn(legend))
        self.next_slide(notes="Рамка — область действия λ. Коралловый y в неё не входит.")
        self.play(Create(box), run_time=0.6)
        for row, n in zip(
            pts,
            [
                "В JS function f(x) { return x + y } — y свободна, её значение даст окружение. Algol 60 перенёс эту лексическую область видимости в языки.",
                "Переименование параметра не меняет смысл. Как rename в IDE.",
                "Если внутри уже есть свой y, а снаружи подставляют чужой y — сначала переименуем внутренний. Ранний Lisp с динамической областью видимости страдал именно от этого бага (funarg problem).",
            ],
        ):
            self.beat(n, FadeIn(row, shift=RIGHT * 0.08))


@slide
class S13_Beta(Talk):
    part = "язык"
    title = "β-редукция: вызов = подстановка"

    def draw(self):
        self.gist("Вызвать функцию — значит *подставить аргумент* на место параметра. Это единственное правило вычисления")
        law = serif("(λx. M) N   →   M [x := N]", 40, INK)
        cap = note("подставить N на все места x в теле M", 21)
        rule = VGroup(law, cap).arrange(DOWN, buff=0.18)
        first = app(
            [("λ", GOLD, "lam"), ("x", GOLD, "p"), (".", INK, "d"), ("x", SKY, "hole")],
            ("y", CORAL, "arg"),
            size=50,
        )
        second = app(
            [
                ("λ", GOLD, "lam"),
                ("x", GOLD, "p"),
                (".", INK, "d1"),
                ("λ", GOLD, "lam2"),
                ("y", GOLD, "y"),
                (".", INK, "d2"),
                ("x", SKY, "hole"),
            ],
            ("a", CORAL, "arg"),
            size=44,
        )
        slot = Rectangle(width=5.0, height=1.1, stroke_width=0, fill_opacity=0)
        left = VGroup(rule, slot).arrange(DOWN, buff=0.55)
        pts = bullets(
            [
                "Вычисление — повторять подстановку, пока есть что подставлять. Как упрощать дробь",
                "Нет памяти, нет команд — только переписывание выражения",
                "Аргумент пришёл не весь? Получится новая функция: *частичное применение*",
            ],
            size=25,
            width=6.2,
        )
        self.split(left, pts, ratio=0.48)
        first.move_to(slot)
        second.move_to(slot)
        self.beat("Вся динамика языка в одной строке. M[x := N] — «M, где x заменили на N».", FadeIn(rule))
        self.beat("Самый короткий вызов. В JS это (x => x)(y).", FadeIn(first), FadeIn(pts[0]))
        self.next_slide(notes="Дать анимации доиграть: y едет на место x, обёртка исчезает. Выражение (λx. M) N называют редексом — reducible expression.")
        result = fly_subst(self, first, "hole", "arg", ["lp", "lam", "p", "d", "rp"])
        self.beat("Как в школьной алгебре: подставили — упростили.", FadeIn(pts[1]))
        self.beat(
            "Функция двух аргументов получила один: подставили a вместо x, λy осталась ждать.",
            FadeOut(result),
            FadeIn(second),
            FadeIn(pts[2]),
        )
        self.next_slide(notes="Итог — λy. a: функция, которая игнорирует аргумент и возвращает a. Скоро она станет TRUE.")
        fly_subst(self, second, "hole", "arg", ["lp", "lam", "p", "d1", "rp"])


@slide
class S13_AlphaEta(Talk):
    part = "язык"
    title = "Три правила переписывания: α, β, η"

    def draw(self):
        self.gist("β считает. α переименовывает параметры. η убирает лишнюю обёртку *x ↦ f(x)*")
        rows = [
            ["α", "λx. M  =  λy. M[x := y]", "имя параметра не важно (см. прошлый слайд)"],
            ["β", "(λx. M) N  →  M[x := N]", "вызов = подстановка"],
            ["η", "λx. f x  =  f", "если x не встречается в f свободно"],
        ]
        grid = table(rows, [0.55, 5.8, 5.2], size=22)
        ex = code_card(
            "const g = f => x => f(x)\n// η: то же, что  f => f\n// (если x не свободен в f)",
            "js",
            size=20,
        )
        z = note("Z для JS — как раз η-обёртка v => x(x)(v), чтобы не вызывать x(x) сразу", 20)
        board = VGroup(grid, ex, z).arrange(DOWN, buff=0.35)
        self.stage(board, buff=0.4)
        self.beat(
            "Карри и Фейс назвали три вида преобразований буквами α, β, η. На практике почти всё — β; α нужна, чтобы подстановка не ломала смысл.",
            FadeIn(grid[0]),
            FadeIn(grid[1]),
        )
        self.beat("β — единственное «настоящее» вычисление. Остальное — про эквивалентные записи одной функции.", FadeIn(grid[2]))
        self.beat(
            "η говорит: обёртка «просто передать арг дальше» ничего не меняет. В строгих языках из неё делают отложенный вызов — вспомните Z на слайде про Y.",
            FadeIn(ex),
            FadeIn(z),
        )


@slide
class S14_Normal(Talk):
    part = "язык"
    title = "Ответ или бесконечность"

    def draw(self):
        self.gist("Вычисление либо приходит к *ответу* — выражению, где нечего подставлять, — либо не кончается никогда")
        stop = VGroup(
            serif("λx. x", 48, MINT),
            note("нормальная форма: подставлять нечего", 22),
        ).arrange(DOWN, buff=0.2)
        spin = Text("↻", font=SANS, font_size=46, color=CORAL)
        loop = VGroup(
            serif("(λx. x x)(λx. x x)", 34, CORAL),
            VGroup(spin, note("Ω переходит сам в себя", 22)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, buff=0.2)
        pair = VGroup(stop, loop).arrange(RIGHT, buff=1.4, aligned_edge=UP)
        self.stage(pair, buff=0.5)
        pts = self.points(
            [
                "*Нормальная форма* — то, что вернула программа",
                "Ω = (λx. x x)(λx. x x): после шага получается он же. Это `while (true)` без while. Источник — самоприменение *x x*",
                "Узнать заранее, кончится ли вычисление, нельзя: это та самая неразрешимость Чёрча",
            ],
            size=25,
            width=11.6,
        )
        self.beat("Слева ответ: подставлять нечего, вычисление закончено.", FadeIn(stop), FadeIn(pts[0]))
        self.beat("Справа Ω — «омега». Подставляем аргумент в x x и получаем исходный терм.", FadeIn(loop))
        self.next_slide(notes="Один оборот. Это не «долго считается» — это не кончается никогда.")
        self.play(Rotate(spin, TAU), run_time=1.1)
        self.beat("Тот же x x, что R(R) у Рассела. Запомните его: в рекурсии он станет двигателем.", FadeIn(pts[1]))
        self.beat("Цена универсальности: язык, где можно всё, неизбежно содержит вечные циклы.", FadeIn(pts[2]))


@slide
class S15_Confluence(Talk):
    part = "язык"
    title = "Чёрч–Россер: порядок не важен"

    def draw(self):
        self.gist("Если ответ есть, он *один* — в каком бы порядке ни делать подстановки")

        def node(text, color=INK):
            return panel(serif(text, 44, color), pad_x=0.34, pad_y=0.18)

        m = node("M")
        n1 = node("N₁", SKY)
        n2 = node("N₂", SKY)
        p = node("P", MINT)
        m.move_to(UP * 1.7)
        n1.move_to(LEFT * 1.6)
        n2.move_to(RIGHT * 1.6)
        p.move_to(DOWN * 1.7)
        a1 = Arrow(m.get_bottom(), n1.get_top(), buff=0.1, color=INK, stroke_width=4)
        a2 = Arrow(m.get_bottom(), n2.get_top(), buff=0.1, color=INK, stroke_width=4)
        b1 = DashedLine(n1.get_bottom(), p.get_top(), buff=0.1, color=MINT, stroke_width=4).add_tip(tip_length=0.24)
        b2 = DashedLine(n2.get_bottom(), p.get_top(), buff=0.1, color=MINT, stroke_width=4).add_tip(tip_length=0.24)
        diamond = VGroup(m, n1, n2, p, a1, a2, b1, b2)
        pts = bullets(
            [
                "В выражении бывает много мест для подстановки, и упрощать их можно в любом порядке",
                "*Теорема (1936):* любые два пути вычисления снова сходятся",
                "Поэтому чистые функции можно считать параллельно и лениво — ответ не изменится. У потоков с общей памятью так не бывает",
            ],
            size=25,
            width=6.8,
        )
        self.split(diamond, pts, ratio=0.4)
        self.beat("Из M можно сделать шаг в разные стороны.", FadeIn(m), GrowArrow(a1), GrowArrow(a2), FadeIn(n1), FadeIn(n2), FadeIn(pts[0]))
        self.beat("Ромб всегда замыкается: найдётся общий P. Это называют конфлюэнтностью — «слиянием».", Create(b1), Create(b2), FadeIn(p), FadeIn(pts[1]))
        self.beat("Компилятор Haskell переставляет вычисления, MapReduce раскидывает их по машинам. Обоснование — здесь. Программа с гонками может дать разные ответы, λ — нет.", FadeIn(pts[2]))


@slide
class S16_Order(Talk):
    part = "язык"
    title = "Стратегии: кто вычисляется первым"

    def draw(self):
        self.gist("Порядок не меняет ответ, но решает, *найдём ли* мы его вообще")
        term = serif("(λx. λy. y)  Ω", 44)
        name = VGroup(
            Text("по имени", font=SANS, font_size=24, color=MINT, weight=BOLD),
            serif("λy. y", 40, MINT),
        ).arrange(DOWN, buff=0.14)
        spin = Text("↻", font=SANS, font_size=46, color=CORAL)
        value = VGroup(
            Text("по значению", font=SANS, font_size=24, color=CORAL, weight=BOLD),
            spin,
        ).arrange(DOWN, buff=0.14)
        pair = VGroup(name, value).arrange(RIGHT, buff=1.2, aligned_edge=UP)
        left = VGroup(term, pair).arrange(DOWN, buff=0.6)
        pts = bullets(
            [
                "*По имени:* сначала вызов, аргумент — только если понадобится. Так считает Haskell",
                "*По значению:* сначала аргументы, потом вызов. JavaScript, Go, Python, Java",
                "Если ответ есть, вычисление по имени его найдёт. В JS ленивы только `&&`, `||` и `?:`",
            ],
            size=25,
            width=6.8,
        )
        self.split(left, pts, ratio=0.4)
        self.beat("Функция выбрасывает свой аргумент. А аргумент — бесконечный Ω.", FadeIn(term))
        self.beat("По имени аргумент не трогают, пока он не нужен. Он не нужен — ответ λy. y.", FadeIn(name), FadeIn(pts[0]))
        self.next_slide(notes="По значению сначала считают Ω — и застревают навсегда.")
        self.play(FadeIn(value), FadeIn(pts[1]), run_time=0.4)
        self.play(Rotate(spin, TAU, about_point=spin.get_center()), run_time=0.9)
        self.beat("Теорема стандартизации. Строгий порядок проще предсказать по памяти и времени — поэтому его выбирает почти каждый язык.", FadeIn(pts[2]))
