from lc.registry import slide
from lc.theme import *
from lc.widgets import *


def _cell(text, color=INK, size=44):
    return panel(serif(text, size, color), pad_x=0.34, pad_y=0.22)


def _pile(n, caption):
    layers = [
        panel(Text("f", font=SERIF, font_size=32, color=GOLD), pad_x=0.26, pad_y=0.14)
        for _ in range(n)
    ]
    layers.append(panel(Text("x", font=SERIF, font_size=32, color=SKY), pad_x=0.26, pad_y=0.14))
    stack = VGroup(*layers).arrange(DOWN, buff=0.1)
    cap = Text(caption, font=SANS, font_size=22, color=MUTED)
    cap.next_to(stack, DOWN, buff=0.14)
    return VGroup(stack, cap)


@slide
class S17_Behavior(Talk):
    part = "данные"
    title = "Данные — это поведение"

    def draw(self):
        self.gist("*Кодирование Чёрча:* значение определяется тем, *что с ним можно сделать*")
        specs = [
            dict(title="булево", tag="выбирает", body="из двух вариантов отдаёт один", accent=MINT),
            dict(title="число n", tag="повторяет", body="применяет действие ровно n раз", accent=GOLD),
            dict(title="пара", tag="отвечает", body="отдаёт обе части тому, кто спросил", accent=SKY),
            dict(title="список", tag="сворачивается", body="это и есть свой reduce", accent=CORAL),
        ]
        cards = tiles(specs, 2.9, size=20)
        grid = VGroup(
            VGroup(*cards[:2]).arrange(RIGHT, buff=0.22),
            VGroup(*cards[2:]).arrange(RIGHT, buff=0.22),
        ).arrange(DOWN, buff=0.22)
        pts = bullets(
            [
                "В языке нет литералов: число, булево, список — это функции",
                "Вопрос «что такое число?» заменяется вопросом «что умеет число?»",
                "Та же идея в ООП: объект — набор ответов на сообщения, как в утиной типизации",
            ],
            size=25,
            width=6.2,
        )
        self.split(grid, pts, ratio=0.48)
        for c, n in zip(
            cards,
            [
                "Булево не хранит бит. Оно умеет выбрать ветку.",
                "Число не цифра. Оно умеет повторить.",
                "Пара не хранит поля. Она отдаёт обе части селектору: FST берёт первую, SND вторую.",
                "Список — это функция, которая сама себя сворачивает. reduce в JS отсюда.",
            ],
        ):
            self.beat(n, FadeIn(c, shift=UP * 0.08))
        for row, n in zip(
            pts,
            [
                "Чёрч придумал это, чтобы показать: арифметика выражается в его языке.",
                "Философский сдвиг: идентичность через поведение, а не через устройство.",
                "Тот, кто писал fold или Visitor, уже пользовался кодированием Чёрча. Дальше два примера крупно: логика и числа.",
            ],
        ):
            self.beat(n, FadeIn(row, shift=RIGHT * 0.08))


@slide
class S18_Bool(Talk):
    part = "данные"
    title = "Булево выбирает"

    def draw(self):
        self.gist("Булево значение — *функция выбора*: TRUE возвращает первый из двух вариантов, FALSE — второй")
        a = _cell("a")
        b = _cell("b")
        boxes = VGroup(a, b).arrange(DOWN, buff=0.38)
        word = serif("TRUE", 46, MINT)
        word.next_to(a, LEFT, buff=0.85)
        row = VGroup(word, boxes)
        defs = VGroup(
            serif("TRUE   =   λt. λf. t", 30),
            serif("FALSE  =   λt. λf. f", 30),
            serif("IF  c  a  b   =   c a b", 30),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        pts = bullets(
            [
                "IF не нужен как конструкция: условие *само* выбирает ветку",
                "Ветвление — это не оператор языка, а обычный вызов функции",
            ],
            size=25,
            width=6.6,
        )
        right = VGroup(defs, pts).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        self.split(row, right, ratio=0.42)
        arrow = Arrow(word.get_right(), a.get_left(), buff=0.14, color=MINT, stroke_width=4)
        word2 = serif("FALSE", 46, CORAL).next_to(b, LEFT, buff=0.85).align_to(word, RIGHT)
        arrow2 = Arrow(word2.get_right(), b.get_left(), buff=0.14, color=CORAL, stroke_width=4)
        self.next_slide(notes="TRUE — функция двух аргументов, которая возвращает первый. Стрелка и есть определение.")
        self.play(FadeIn(row), GrowArrow(arrow), FadeIn(defs[0]), run_time=0.7)
        self.play(a[0].animate.set_stroke(MINT, width=4), b.animate.set_opacity(0.28), run_time=0.45)
        self.next_slide(notes="FALSE возвращает второй. Обратите внимание: это та же λy. a, что получилась на слайде про β.")
        self.play(
            ReplacementTransform(word, word2),
            ReplacementTransform(arrow, arrow2),
            a[0].animate.set_stroke(LINE, width=1.4),
            a.animate.set_opacity(0.28),
            b.animate.set_opacity(1),
            b[0].animate.set_stroke(CORAL, width=4),
            FadeIn(defs[1]),
            run_time=0.8,
        )
        self.beat("IF ничего не выбирает сам: он отдаёт обе ветки тому, кто умеет выбирать — самому условию.", FadeIn(defs[2]))
        for row_, n in zip(
            pts,
            [
                "Как тернарный оператор, только без оператора.",
                "Так же определяются NOT (поменять варианты местами) и AND = λp. λq. p q p.",
            ],
        ):
            self.beat(n, FadeIn(row_, shift=RIGHT * 0.08))


@slide
class S19_Numbers(Talk):
    part = "данные"
    title = "Число повторяет"

    def draw(self):
        self.gist("Число n — это «повторить действие n раз». Ноль — не делать ничего")
        cols = VGroup(_pile(0, "ноль"), _pile(1, "один"), _pile(2, "два")).arrange(
            RIGHT, buff=0.7, aligned_edge=DOWN
        )
        forms = VGroup(
            serif("n  =  λf. λx. f (f (… f x))", 28),
            serif("SUCC  =  λn. λf. λx. f (n f x)", 28),
            serif("ADD   =  λm. λn. m SUCC n", 28),
        ).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        pts = bullets(
            [
                "+1 — добавить ещё один слой f. Сложение — повторить «+1» m раз",
                "Проверка в JS: `two(n => n + 1)(0)` даёт 2",
            ],
            size=25,
            width=6.8,
        )
        right = VGroup(forms, pts).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        self.split(cols, right, ratio=0.36)
        extra = panel(Text("f", font=SERIF, font_size=32, color=GOLD), pad_x=0.26, pad_y=0.14)
        extra.next_to(cols[2][0], UP, buff=0.1)
        three = Text("три", font=SANS, font_size=22, color=GOLD)
        three.move_to(cols[2][1])
        self.beat(
            "Ноль — x, к которому не притронулись. Каждое следующее число — ещё один вызов f.",
            LaggedStart(FadeIn(cols[0]), FadeIn(cols[1]), FadeIn(cols[2]), lag_ratio=0.35),
            FadeIn(forms[0]),
            run_time=1.5,
        )
        self.beat(
            "Прибавить один — повесить ещё один f сверху. Число не вскрывают, как цифру.",
            FadeIn(extra, shift=DOWN * 0.2),
            FadeOut(cols[2][1]),
            FadeIn(three),
            FadeIn(forms[1]),
            run_time=0.8,
        )
        self.beat("Сложить — повторить этот жест m раз, начиная с n.", FadeIn(forms[2]))
        for row, n in zip(
            pts,
            [
                "Вычитание тоже кодируется, но терм для «−1» длинный и хитрый. Сам Чёрч сомневался, что он существует; Клини нашёл его в 1932 году — по его собственному рассказу, в кресле у зубного врача.",
                "Если передать вместо f инкремент, а вместо x ноль — получится обычное число. Так кодирование проверяют.",
            ],
        ):
            self.beat(n, FadeIn(row, shift=RIGHT * 0.08))
