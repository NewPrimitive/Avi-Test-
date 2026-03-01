#!/usr/bin/env python3
"""Audio Word Puzzle game.

Players listen to word parts and combine them into a full word.
"""

from __future__ import annotations

import json
import random
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
AUDIO_PUZZLES_PATH = BASE_DIR / "audio_puzzles.json"
DEFAULT_ROUNDS = 5


VOICE_COMMANDS: list[list[str]] = [
    ["say"],
    ["espeak"],
    ["spd-say"],
]


def load_audio_puzzles(path: Path = AUDIO_PUZZLES_PATH) -> list[dict[str, Any]]:
    """Load and validate audio puzzles from JSON."""
    with path.open("r", encoding="utf-8") as file:
        puzzles = json.load(file)

    if not isinstance(puzzles, list) or not puzzles:
        raise ValueError("audio_puzzles.json must contain a non-empty list of puzzles.")

    required_keys = {"prompt", "parts", "answer", "hint", "explanation"}
    for index, puzzle in enumerate(puzzles, start=1):
        if not isinstance(puzzle, dict):
            raise ValueError(f"Puzzle #{index} must be an object.")

        if not required_keys.issubset(puzzle):
            missing = required_keys - set(puzzle)
            raise ValueError(f"Puzzle #{index} missing keys: {', '.join(sorted(missing))}")

        parts = puzzle["parts"]
        if not isinstance(parts, list) or not parts or any(not isinstance(part, str) for part in parts):
            raise ValueError(f"Puzzle #{index} has invalid 'parts'. It must be a list of words/syllables.")

    return puzzles


def normalize_answer(answer: str) -> str:
    """Normalize answers for case-insensitive comparison."""
    return " ".join(answer.strip().lower().split())


def find_voice_command() -> list[str] | None:
    """Return the first available text-to-speech command."""
    for command in VOICE_COMMANDS:
        if shutil.which(command[0]):
            return command
    return None


def speak_text(text: str, voice_command: list[str] | None) -> None:
    """Speak text if a TTS command is available, otherwise print fallback text."""
    if voice_command is None:
        print(f"🔊 (audio fallback) {text}")
        return

    try:
        subprocess.run([*voice_command, text], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError:
        print(f"🔊 (audio fallback) {text}")


def play_parts(parts: list[str], voice_command: list[str] | None) -> None:
    """Play/speak each word part with a short pause."""
    for part in parts:
        speak_text(part, voice_command)
        time.sleep(0.5)


def ask_audio_puzzle(
    puzzle: dict[str, Any],
    number: int,
    total: int,
    voice_command: list[str] | None,
) -> bool:
    """Ask one audio puzzle. Return True if solved."""
    print(f"\nPuzzle {number}/{total} (audio word puzzle)")
    print(puzzle["prompt"])

    max_attempts = 2
    for attempt in range(1, max_attempts + 1):
        input("Press Enter to hear the parts...")
        play_parts(puzzle["parts"], voice_command)
        guess = input("What word do those parts make? ")

        if normalize_answer(guess) == normalize_answer(str(puzzle["answer"])):
            print("✅ Nice solve!")
            return True

        if attempt == 1:
            print(f"💡 Hint: {puzzle['hint']}")
            print("Let's hear it one more time.")

    print(f"❌ Good try. Correct answer: {puzzle['answer']}")
    print(f"📘 {puzzle['explanation']}")
    return False


def run_game() -> None:
    """Run the audio word puzzle game."""
    print("🎧 Welcome to the Audio Word Puzzle Game!")
    player_name = input("What is your name? ").strip() or "Player"

    voice_command = find_voice_command()
    if voice_command is None:
        print("⚠️ No text-to-speech command found. Falling back to printed audio clues.")
    else:
        print(f"Using voice command: {voice_command[0]}")

    puzzles = load_audio_puzzles()
    rounds = min(DEFAULT_ROUNDS, len(puzzles))
    selected_puzzles = random.sample(puzzles, rounds)

    score = 0
    for number, puzzle in enumerate(selected_puzzles, start=1):
        if ask_audio_puzzle(puzzle, number, rounds, voice_command):
            score += 1

    print("\n=== Results ===")
    print(f"{player_name}, you solved {score}/{rounds} audio puzzles.")

    if score == rounds:
        print("🏆 Perfect score! Audio puzzle champion!")
    elif score >= rounds - 1:
        print("🌟 Great listening! Almost perfect.")
    else:
        print("👏 Nice effort! Try again and keep training your ears.")


if __name__ == "__main__":
    try:
        run_game()
    except KeyboardInterrupt:
        print("\nGame ended. See you next time!")
        sys.exit(0)
