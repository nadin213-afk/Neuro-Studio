#!/usr/bin/env python3
"""Генератор идей Instagram-постов об EFT-терапии.

Анализирует существующие посты, определяет стиль автора
и генерирует новые идеи через Claude API.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

MODEL = "claude-sonnet-4-5-20250929"


def read_posts(posts_dir: Path) -> list[dict[str, str]]:
    """Прочитать все .txt файлы из папки с постами."""
    posts = []
    if not posts_dir.exists():
        print(f"Ошибка: папка {posts_dir} не найдена.")
        sys.exit(1)

    for filepath in sorted(posts_dir.glob("*.txt")):
        text = filepath.read_text(encoding="utf-8").strip()
        if text:
            posts.append({"filename": filepath.name, "text": text})

    if not posts:
        print(f"Ошибка: нет .txt файлов с текстом в {posts_dir}")
        sys.exit(1)

    return posts


def format_posts_for_prompt(posts: list[dict[str, str]]) -> str:
    """Собрать тексты постов в единый блок для промпта."""
    parts = []
    for i, post in enumerate(posts, 1):
        parts.append(f"--- Пост {i} ({post['filename']}) ---\n{post['text']}")
    return "\n\n".join(parts)


def analyze_style(client: anthropic.Anthropic, posts_block: str) -> str:
    """Запрос 1: анализ стилистических паттернов автора."""
    print("Анализирую стиль постов...")
    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": (
                    "Ты — эксперт по копирайтингу и стилистике текстов для соцсетей.\n\n"
                    "Проанализируй следующие Instagram-посты одного автора на тему EFT-терапии. "
                    "Выдели ключевые стилистические паттерны:\n"
                    "- Тон и голос (формальный/неформальный, тёплый/экспертный и т.д.)\n"
                    "- Ритм и структура текста (длина предложений, абзацы, списки)\n"
                    "- Излюбленные приёмы (вопросы к читателю, метафоры, истории, призывы)\n"
                    "- Тематические паттерны (какие аспекты EFT чаще затрагиваются)\n"
                    "- Характерная лексика и обороты\n\n"
                    "Посты:\n\n"
                    f"{posts_block}\n\n"
                    "Дай структурированный анализ на русском языке."
                ),
            }
        ],
    )
    return response.content[0].text


def generate_ideas(
    client: anthropic.Anthropic,
    posts_block: str,
    style_analysis: str,
    count: int,
    topic: str | None,
) -> str:
    """Запрос 2: генерация идей постов в стиле автора."""
    print(f"Генерирую {count} идей...")

    topic_instruction = ""
    if topic:
        topic_instruction = f"\nФокусируйся на теме: «{topic}».\n"

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": (
                    "Ты — креативный копирайтер, специализирующийся на контенте "
                    "об EFT-терапии (Emotionally Focused Therapy) для Instagram.\n\n"
                    "Вот анализ стиля автора:\n\n"
                    f"{style_analysis}\n\n"
                    "Вот примеры постов автора:\n\n"
                    f"{posts_block}\n\n"
                    f"Сгенерируй {count} идей для новых Instagram-постов в стиле этого автора. "
                    "Каждая идея должна содержать:\n"
                    "- Заголовок (короткий, цепляющий)\n"
                    "- Полный текст поста, готовый к публикации\n"
                    "- 3-5 хештегов\n\n"
                    "Сохраняй стиль, тон и подход автора. "
                    "Идеи должны быть разнообразными и практически полезными для аудитории."
                    f"{topic_instruction}\n\n"
                    "Формат ответа:\n"
                    "### 1. [Заголовок]\n[Текст поста]\n\n"
                    "Хештеги: #... #... #...\n\n"
                    "---\n"
                ),
            }
        ],
    )
    return response.content[0].text


def save_output(
    output_dir: Path, style_analysis: str, ideas: str, topic: str | None
) -> Path:
    """Сохранить результат в markdown-файл."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"ideas_{timestamp}.md"
    filepath = output_dir / filename

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    topic_line = f" | Тема: {topic}" if topic else ""

    content = (
        f"# Идеи постов EFT-терапия — {now}{topic_line}\n\n"
        f"## Анализ стиля\n\n{style_analysis}\n\n"
        f"## Идеи постов\n\n{ideas}\n"
    )

    filepath.write_text(content, encoding="utf-8")
    return filepath


def main():
    parser = argparse.ArgumentParser(
        description="Генератор идей Instagram-постов об EFT-терапии"
    )
    parser.add_argument(
        "--posts-dir",
        type=Path,
        default=Path("./posts"),
        help="Папка с .txt файлами постов (по умолчанию ./posts)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("./output"),
        help="Папка для результатов (по умолчанию ./output)",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="Тема для фокусировки (например, 'стыд', 'созависимость')",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=10,
        help="Количество идей (по умолчанию 10)",
    )
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Ошибка: установите переменную окружения ANTHROPIC_API_KEY")
        sys.exit(1)

    posts = read_posts(args.posts_dir)
    print(f"Найдено {len(posts)} постов.")

    posts_block = format_posts_for_prompt(posts)
    client = anthropic.Anthropic(api_key=api_key)

    style_analysis = analyze_style(client, posts_block)
    ideas = generate_ideas(client, posts_block, style_analysis, args.count, args.topic)

    filepath = save_output(args.output_dir, style_analysis, ideas, args.topic)
    print(f"Готово! Результат сохранён в {filepath}")


if __name__ == "__main__":
    main()
