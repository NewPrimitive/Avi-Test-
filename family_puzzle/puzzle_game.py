#!/usr/bin/env python3
"""Family Puzzle Game.

A beginner-friendly terminal game where players solve logic and word puzzles.
"""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
PUZZLES_PATH = BASE_DIR / "puzzles.json"
DEFAULT_ROUNDS = 5


def load_puzzles(path: Path = PUZZLES_PATH) -> list[dict[str, Any]]:
    """Load and validate puzzles from JSON."""
    with path.open("r", encoding="utf-8") as file:
        puzzles = json.load(file)

    if not isinstance(puzzles, list) or not puzzles:
        raise ValueError("puzzles.json must contain a non-empty list of puzzles.")

    required_keys = {"type", "prompt", "answer", "hint", "explanation"}
    valid_types = {"word", "math", "logic"}

    for index, puzzle in enumerate(puzzles, start=1):
        if not isinstance(puzzle, dict):
            raise ValueError(f"Puzzle #{index} must be an object.")

        if not required_keys.issubset(puzzle.keys()):
            missing = required_keys - set(puzzle.keys())
            raise ValueError(f"Puzzle #{index} missing keys: {', '.join(sorted(missing))}")

        if puzzle["type"] not in valid_types:
            raise ValueError(f"Puzzle #{index} has invalid type '{puzzle['type']}'.")

    return puzzles


def normalize_answer(answer: str) -> str:
    """Normalize a player or puzzle answer for case-insensitive matching."""
    return " ".join(answer.strip().lower().split())


def ask_puzzle(puzzle: dict[str, Any], number: int, total: int) -> bool:
    """Ask one puzzle. Return True if player solves it."""
    print(f"\nPuzzle {number}/{total} ({puzzle['type']})")
    print(puzzle["prompt"])

    max_attempts = 2
    for attempt in range(1, max_attempts + 1):
        guess = input("Your answer: ")

        if normalize_answer(guess) == normalize_answer(str(puzzle["answer"])):
            print("✅ Nice solve!")
            return True

        if attempt == 1:
            print(f"💡 Hint: {puzzle['hint']}")
            print("Try once more!")

    print(f"❌ Good try. Correct answer: {puzzle['answer']}")
    print(f"📘 {puzzle['explanation']}")
    return False


def run_game() -> None:
    """Run the puzzle game."""
    print("🧩 Welcome to the Family Puzzle Game!")
    player_name = input("What is your name? ").strip() or "Player"

    puzzles = load_puzzles()
    rounds = min(DEFAULT_ROUNDS, len(puzzles))
    selected_puzzles = random.sample(puzzles, rounds)

    score = 0
    for number, puzzle in enumerate(selected_puzzles, start=1):
        if ask_puzzle(puzzle, number, rounds):
            score += 1

    print("\n=== Results ===")
    print(f"{player_name}, you solved {score}/{rounds} puzzles.")

    if score == rounds:
        print("🏆 Perfect score! Puzzle master!")
    elif score >= rounds - 1:
        print("🌟 Great job! Almost perfect.")
    else:
        print("👏 Nice effort! Keep practicing and play again.")


if __name__ == "__main__":
    run_game()
