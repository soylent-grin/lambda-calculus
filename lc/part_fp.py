from lc.registry import slide
from lc.theme import *
from lc.widgets import *


@slide
class S29_Compiler(Talk):
    part = "практика"
    title = "λ и типы внутри компилятора"

    def draw(self):
        self.gist("Компилятор сводит программу к типизированному λ, проверяет типы и лишь потом спускается к машине")
        rows = [
            ["этап", "что происходит  (связь с лекцией)"],
            ["1. убрать сахар", "let, if, циклы → функции и вызовы  (язык = λ + сахар)"],
            ["2. проверить типы", "ошибка типа = неверное доказательство  (Карри–Ховард)"],
            ["3. оптимизировать", "встроить функцию = сделать β-шаг  (Чёрч–Россер)"],
            ["4. замыкания", "свободные имена уезжают в окружение"],
            ["5. машинный код", "регистры и стек вместо подстановки  (Тьюринг)"],
        ]
        grid = table(rows, [3.2, 8.8], size=25)
        self.stage(grid, buff=0.4)
        self.beat("Так устроены GHC (Haskell → Core, типизированное λ), OCaml, Scala. Замыкания и SSA — те же идеи — есть и в V8, и в LLVM.", FadeIn(grid[0]))
        notes = [
            "Ландин, «The Next 700 Programming Languages» (1966): любой язык — λ-ядро плюс синтаксический сахар.",
            "Компилятор с типами — это проверщик доказательств из прошлого слайда. TypeScript и Rust делают то же, с оговорками.",
            "Inlining — это буквально β-редукция. Чёрч–Россер гарантирует, что порядок оптимизаций не меняет результат чистого кода.",
            "Closure conversion: x => x + n превращается в пару «код + окружение {n}». Похожим образом V8 хранит захваченные переменные в объекте-контексте.",
            "Последний шаг — мост Чёрч–Тьюринг, который компилятор перестраивает при каждой сборке.",
        ]
        for row, n in zip(grid[1:], notes):
            self.beat(n, FadeIn(row, shift=UP * 0.05))


@slide
class S30_FP(Talk):
    part = "практика"
    title = "Функциональное программирование"

    def draw(self):
        self.gist("*ФП* — писать программы как λ-выражения: из чистых функций и без изменения данных")
        specs = [
            dict(
                head=code_card("sq(3) + sq(3)\n// всегда 18", "js", size=20),
                title="Чистые функции",
                tag="как β-подстановка",
                body="вызов можно заменить результатом: легко тестировать и распараллеливать",
                accent=GOLD,
            ),
            dict(
                head=code_card("orders\n  .filter(o => o.paid)\n  .map(o => o.sum)", "js", size=20),
                title="Функции — значения",
                tag="как λ",
                body="map, filter, reduce вместо циклов с индексом",
                accent=SKY,
            ),
            dict(
                head=code_card("{ ...state, done: true }\n// state не тронут", "js", size=20),
                title="Неизменяемость",
                tag="нет присваивания",
                body="новые данные вместо правок: нет гонок, есть undo",
                accent=MINT,
            ),
        ]
        cards = tiles(specs, 4.0, size=22).arrange(RIGHT, buff=0.3)
        self.stage(cards, buff=0.45)
        notes = [
            "Ссылочная прозрачность: sq(3) можно заменить на 9, и смысл программы не изменится. С функцией, которая меняет внешний счётчик, так нельзя.",
            "Функции высшего порядка: «оставь оплаченные, возьми суммы». reduce — это список Чёрча, «сверни меня».",
            "Redux, React state, Clojure, Immer. Новые версии структуры разделяют общие части, поэтому копировать всё не нужно.",
        ]
        for c, n in zip(cards, notes):
            self.beat(n, FadeIn(c, shift=UP * 0.08))


@slide
class S31_Effects(Talk):
    part = "практика"
    title = "Граница: эффекты снаружи ядра"

    def draw(self):
        self.gist("Чистое λ не умеет ввод-вывод. ФП не запрещает эффекты, а *выносит их на край* программы")
        words = VGroup(
            Text("состояние", font=SANS, font_size=36, color=GOLD, weight=BOLD),
            Text("ввод-вывод", font=SANS, font_size=36, color=SKY, weight=BOLD),
            Text("время", font=SANS, font_size=36, color=MINT, weight=BOLD),
            Text("гонки", font=SANS, font_size=36, color=CORAL, weight=BOLD),
        ).arrange(RIGHT, buff=0.7)
        self.stage(words, buff=0.5)
        pts = self.points(
            [
                "*Монада* — эффект как значение: описание действия, которое выполнит среда. Так устроен `IO` в Haskell",
                "Promise и async/await в JS — та же идея: описание вычисления, которое запустят позже",
                "Архитектура «чистое ядро, эффекты по краям»: внутри ядра работают и Чёрч–Россер, и тесты",
            ],
            size=25,
            width=11.6,
        )
        self.beat("Всё, ради чего пишут реальные программы, — снаружи трёх форм.", LaggedStart(*[FadeIn(w) for w in words], lag_ratio=0.2), run_time=1.0)
        for row, n in zip(
            pts,
            [
                "Моджи (1989) и Вадлер. Программа на Haskell — чистая функция, которая возвращает план действий. Выполняет план рантайм.",
                "Promise не совсем монада по законам, но мысль та же.",
                "Functional core, imperative shell — Гэри Бернхардт. Прямое следствие всей лекции.",
            ],
        ):
            self.beat(n, FadeIn(row, shift=RIGHT * 0.08))
