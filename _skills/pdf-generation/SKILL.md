---
name: pdf-generation
version: 1.0.0
description: |
  Генерация PDF-документов из markdown: чек-листы, гайды,
  лид-магниты для аудитории. Поддержка русского языка.
  Используй когда нужно: создать скачиваемый PDF,
  оформить лид-магнит, сделать раздаточный материал.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# PDF Generation — для @psy_eft

Создание профессиональных PDF на русском языке для лид-магнитов и раздаточных материалов.

## Зависимости

```bash
# macOS
brew install pandoc
brew install --cask mactex
```

## Быстрый старт

```bash
# Русский PDF, мобильный формат (для Telegram)
pandoc document.md -o document.pdf \
  --pdf-engine=xelatex \
  -V mainfont="EB Garamond" \
  -V geometry:paperwidth=6in \
  -V geometry:paperheight=9in \
  -V geometry:margin=0.5in \
  -V fontsize=10pt \
  -V linestretch=1.2

# Русский PDF, A4 (для печати)
pandoc document.md -o document.pdf \
  --pdf-engine=xelatex \
  --toc --toc-depth=2 \
  -V mainfont="EB Garamond" \
  -V geometry:margin=2.5cm \
  -V fontsize=11pt
```

## Типы документов для @psy_eft

### 1. Лид-магнит (чек-лист / гайд)
Цель: скачивание в обмен на подписку.
Формат: мобильный (6x9), 1–3 страницы.
Цвет темы: зелёный (059669).

```yaml
---
title: "5 вопросов, чтобы понять свой тип привязанности"
subtitle: "Мини-гайд от Надежды Жеманцевой"
author: "Надежда Жеманцева | @psy_eft"
date: "2026"
titlepage: true
titlepage-color: "059669"
titlepage-text-color: "ffffff"
---
```

### 2. Раздаточный материал для интенсива "Твоя Точка Зрения"
Цель: выдать участницам после сессии.
Формат: A4, 2–4 страницы.
Цвет темы: фиолетовый (7c3aed).

```yaml
---
title: "Твоя Точка Зрения — рабочая тетрадь"
subtitle: "Инсайт-сессия с МАК-картами"
author: "Надежда Жеманцева"
titlepage: true
titlepage-color: "7c3aed"
titlepage-text-color: "ffffff"
---
```

### 3. Информационный гайд
Цель: экспертный контент для блога / рассылки.
Формат: мобильный или A4.
Цвет темы: синий (1e3a8a).

## Рабочий процесс

### Шаг 1: Напиши контент в markdown
Используй навык `lead-magnet` или `content-research-writer` для создания текста.
Соблюдай voice.md.

### Шаг 2: Добавь YAML frontmatter
Выбери шаблон из типов выше.

### Шаг 3: Проверь markdown
- Пустая строка перед списками (обязательно для Pandoc)
- Пустая строка после заголовков
- Вложенные списки: 3 пробела

### Шаг 4: Генерируй PDF
```bash
pandoc document.md -o document.pdf \
  --pdf-engine=xelatex \
  -V mainfont="EB Garamond" \
  -V geometry:paperwidth=6in \
  -V geometry:paperheight=9in \
  -V geometry:margin=0.5in \
  -V fontsize=10pt \
  -V linestretch=1.2
```

### Шаг 5: Проверь и отправь
- Открой PDF, проверь вёрстку
- Отправь через Telegram-бот или прикрепи к посту

## Сохранение
- Лид-магниты: briefs/leadmagnet_[название].md + .pdf
- Раздатки: briefs/handout_[название].md + .pdf

## Советы

- Для мобильного чтения (Telegram) — всегда 6x9
- EB Garamond отлично работает с русским текстом
- Не перегружай: лид-магнит = 1–3 страницы максимум
- Добавь контакт внизу каждой страницы: @psy_eft | zhemantceva.co
