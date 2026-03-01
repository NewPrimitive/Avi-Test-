#!/usr/bin/env python3
"""Lily Quiz Game.

A simple terminal quiz game with KATSEYE and K-Pop Demon Hunters themed questions.
"""

from __future__ import annotations

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
QUESTIONS_PATH = BASE_DIR / "questions.json"
HIGHSCORES_PATH = BASE_DIR / "highscores.json"
DEFAULT_QUESTION_COUNT = 10
MAX_HIGHSCORES = 10


def load_questions(path: Path = QUESTIONS_PATH) -> list[dict[str, Any]]:
    """Load and validate quiz questions from JSON."""
    with path.open("r", encoding="utf-8") as file:
        questions = json.load(file)

    if not isinstance(questions, list) or not questions:
        raise ValueError("questions.json must contain a non-empty list of questions.")

    for index, question in enumerate(questions, start=1):
        if not isinstance(question, dict):
            raise ValueError(f"Question #{index} must be an object.")

        required_keys = {"question", "choices", "answer", "explanation"}
        if not required_keys.issubset(question.keys()):
            missing = required_keys - set(question.keys())
            raise ValueError(f"Question #{index} missing keys: {', '.join(sorted(missing))}")

        if not isinstance(question["choices"], list) or len(question["choices"]) < 2:
            raise ValueError(f"Question #{index} must have at least 2 choices.")

        answer = question["answer"]
        if not isinstance(answer, int) or not (1 <= answer <= len(question["choices"])):
            raise ValueError(
                f"Question #{index} answer must be a number from 1 to {len(question['choices'])}."
            )

    return questions


def prompt_int(prompt: str, minimum: int, maximum: int) -> int:
    """Prompt until a valid integer in [minimum, maximum] is entered."""
    while True:
        raw_value = input(prompt).strip()
        if not raw_value.isdigit():
            print("Please enter a number.")
            continue

        value = int(raw_value)
        if minimum <= value <= maximum:
            return value

        print(f"Please choose a number from {minimum} to {maximum}.")


def ask_question(question: dict[str, Any], number: int, total: int) -> bool:
    """Ask one question and return True if the player answers correctly."""
    print(f"\nQuestion {number}/{total}")
    print(question["question"])

    for index, choice in enumerate(question["choices"], start=1):
        print(f"  {index}. {choice}")

    guess = prompt_int("Your answer: ", 1, len(question["choices"]))
    correct_answer = question["answer"]

    if guess == correct_answer:
        print("✅ Correct!")
        return True

    correct_choice = question["choices"][correct_answer - 1]
    print(f"❌ Not quite. The correct answer was: {correct_choice}")
    print(f"💡 {question['explanation']}")
    return False


def load_highscores(path: Path = HIGHSCORES_PATH) -> list[dict[str, Any]]:
    """Load highscores file if present; otherwise return an empty list."""
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        return []

    safe_scores: list[dict[str, Any]] = []
    for item in data:
        if isinstance(item, dict) and {"name", "score", "total", "date"}.issubset(item):
            safe_scores.append(item)
    return safe_scores


def save_highscores(scores: list[dict[str, Any]], path: Path = HIGHSCORES_PATH) -> None:
    """Save highscores list to JSON file."""
    with path.open("w", encoding="utf-8") as file:
        json.dump(scores, file, indent=2)


def show_highscores(scores: list[dict[str, Any]]) -> None:
    """Print highscores in rank order."""
    print("\n🏆 High Scores")
    if not scores:
        print("No high scores yet. Be the first!")
        return

    for rank, entry in enumerate(scores, start=1):
        print(f"{rank:>2}. {entry['name']} - {entry['score']}/{entry['total']} ({entry['date']})")


def run_quiz() -> None:
    """Main game loop."""
    print("🎮 Welcome to Lily Quiz!")
    player_name = input("What is your name? ").strip() or "Player"

    questions = load_questions()
    question_count = min(DEFAULT_QUESTION_COUNT, len(questions))
    selected_questions = random.sample(questions, question_count)

    score = 0
    for number, question in enumerate(selected_questions, start=1):
        if ask_question(question, number, question_count):
            score += 1

    print("\n=== Final Score ===")
    print(f"{player_name}, you scored {score}/{question_count}.")

    highscores = load_highscores()
    highscores.append(
        {
            "name": player_name,
            "score": score,
            "total": question_count,
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
    )

    highscores.sort(key=lambda entry: (entry["score"], -entry["total"]), reverse=True)
    highscores = highscores[:MAX_HIGHSCORES]
    save_highscores(highscores)
    show_highscores(highscores)


if __name__ == "__main__":
    run_quiz()
