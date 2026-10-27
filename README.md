# Введение в λ-исчисление

Лекция для разработчиков: слайды Manim и песочница с пошаговой β-редукцией.
Примеры на JavaScript, Haskell и Go.

Зависимости ставятся через [uv](https://docs.astral.sh/uv/). Нужен системный `ffmpeg`, Cairo и Pango. Формулы рисуются шрифтами, LaTeX не нужен.

```bash
UV_PYTHON_PREFERENCE=only-managed uv sync
```

`only-managed` нужен, если системный Python собран без заголовков: иначе Cairo не соберётся.

## Слайды

Рендер всех сцен, по умолчанию 1920×1080, 30 кадров/с:

```bash
./scripts/render.sh
```

Черновик быстрее:

```bash
./scripts/render.sh -ql
```

Показ в окне, вперёд стрелкой вправо. Заметки докладчика в HTML-версии открываются клавишей `S`.

```bash
./scripts/present.sh
./scripts/export-html.sh
```

`export-html.sh` собирает `talk.html` из уже отрендеренных сцен.

## GitHub Pages

После рендера и экспорта HTML:

```bash
./scripts/render.sh          # или только изменённые сцены
./scripts/export-html.sh
./scripts/check-pages-ready.sh   # все mp4 на месте, _site собран
```

Локально открыть то же, что уедет на Pages:

```bash
./scripts/build-pages.sh
python3 -m http.server --directory _site 8080
# http://localhost:8080/  и  http://localhost:8080/playground/
```

В репозитории на GitHub: **Settings → Pages → Build and deployment → GitHub Actions**. При push в `main` workflow публикует сайт: **корень `/` — слайды** (`talk.html` копируется в `index.html`), **`/playground/` — песочница**. Файл `talk.html` дублируется для прямых ссылок. На слайдах в углу — ссылка «Песочница».

### Что коммитить для GitHub Pages

Workflow **не** запускает `./scripts/render.sh` — только `./scripts/build-pages.sh` из уже лежащих в репо файлов. Перед push:

```bash
./scripts/export-html.sh   # после render, если меняли слайды
git add talk.html talk_assets/ playground/
```

| В git | Назначение |
|-------|------------|
| `talk.html` | слайды (в CI → `index.html`) |
| `talk_assets/` | видео (~30 MB) |
| `playground/` | песочница |
| `.github/workflows/pages.yml` | деплой |

Не нужны для сайта: `media/`, `slides/`, `_site/`, `.venv/` (см. `.gitignore`). Исходники `lc/`, `presentation.py` — для разработки; на Pages не попадают, но в репо их обычно держат.

## Песочница

```bash
./scripts/playground.sh
```

Открыть <http://localhost:8765>. 21 урок в семи главах: основы, логика, числа, пары и списки, бесконечность и порядок, рекурсия, свободное плавание. В каждом уроке — идея, «на что смотреть» и «попробуйте». Стрелка вправо делает шаг, влево — отменяет. Режим «по имени» не трогает неиспользуемый аргумент, «по значению» считает его сразу. Ссылка `#N` открывает урок N.

Проверка редуктора:

```bash
node --test playground/reducer.test.mjs
```
