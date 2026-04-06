---
name: telegram-publisher
version: 2.0.0
description: |
  Подготовка и публикация постов в Telegram-канал @psychologicalZN.
  Используй когда нужно: отформатировать пост для Telegram,
  подготовить к отправке через бот, проверить длину и разметку,
  опубликовать черновик. Включает multi-part разбивку, проверку
  форматирования и пост-паблиш процесс.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Telegram Publisher v2 — для @psychologicalZN

Подготовка, проверка и публикация постов в Telegram.
Перед написанием текста ОБЯЗАТЕЛЬНО прочитай _style/voice.md.

## Настройки канала

- Канал: @psychologicalZN
- Бот: @NadiapsyEft_bot
- Chat ID: 249945037
- Webhook: https://hook.eu1.make.com/1gewptd46asoj4gio53uzduud4hm898r

## Форматирование для Telegram (HTML)

```html
<b>жирный</b>
<i>курсив</i>
<a href="https://t.me/psychologicalZN">ссылка</a>
```

Правила:
- Только HTML — без Markdown
- Пустая строка = новый абзац
- Без эмодзи в тексте (минимально в CTA)

## Структура файла черновика

```markdown
---
date: YYYY-MM-DD
status: draft
type: post | ad | promo | announce
channel: psychologicalZN
---

[Текст поста в HTML-разметке]
```

Статусы: `draft` → `ready` → `published`

## Лимиты по типам

| Тип | Макс. символов | Файл |
|-----|---------------|------|
| Обычный пост | 4096 | telegram/tg_NN.txt |
| Рекламный пост | 600 | telegram/tg_ad_NN.txt |
| Анонс | 800 | telegram/tg_announce_NN.txt |

## Multi-part сообщения

Если пост длиннее 4096 символов — разбей на части через разделитель `---`.
Каждая часть отправляется отдельным сообщением.

```
[Часть 1 — до 4096 символов]

---

[Часть 2 — продолжение]
```

## Проверка перед отправкой

### 1. Длина
```bash
CHARS=$(wc -m < telegram/tg_NN.txt)
echo "$CHARS символов"
```

### 2. Форматирование (КРИТИЧНО)
Проверь что нет "сырого" Markdown:
- Нет `**жирный**` → должно быть `<b>жирный</b>`
- Нет `*курсив*` → должно быть `<i>курсив</i>`
- Нет `[текст](url)` → должно быть `<a href="url">текст</a>`
- Нет `# заголовок` → должно быть `<b>заголовок</b>`

Если найдены остатки Markdown — НЕ ОТПРАВЛЯТЬ. Исправить сначала.

### 3. Стоп-слова
Проверь отсутствие: "я здесь", "эффективный", "уникальный", лишних восклицательных знаков.

### 4. Humanizer
Пропусти через _skills/humanizer/ перед финализацией.

## Рабочий процесс

### Шаг 1: Черновик
Сохрани в telegram/tg_NN.txt. Установи status: draft.

### Шаг 2: Проверка
Длина OK? Форматирование OK? Стоп-слова OK? Humanizer пройден?
→ Установи status: ready.

### Шаг 3: Предпросмотр (отправка себе)
```bash
curl -X POST "https://hook.eu1.make.com/1gewptd46asoj4gio53uzduud4hm898r" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "249945037",
    "text": "ТЕКСТ ПОСТА",
    "parse_mode": "HTML"
  }'
```

### Шаг 4: Публикация
После подтверждения → отправить в канал.
Обнови frontmatter: status: published, published_date: YYYY-MM-DD.

## Пост-паблиш (автоматически)
После публикации в канал:
1. Обнови status на `published` и добавь `published_date`
2. Если есть папка `telegram/published/` — переместь туда
3. Добавь запись в `telegram/index.md` (если есть)

## Адаптация из Instagram

1. Убери хештеги
2. Сократи на 30–40%
3. Замени "пишите в ЛС" → "напишите мне @psychologicalZN"
4. Добавь 1–2 личные строки
5. Проверь длину
6. Оберни в HTML

## Подвал для постов канала

```html
<a href="https://t.me/psychologicalZN">@psychologicalZN</a> | Надежда Жеманцева
```
