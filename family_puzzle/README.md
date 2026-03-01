# Family Puzzle Game

A beginner-friendly puzzle game for parents and kids to play in the terminal.

## Quick start (from repository root)

```bash
python3 family_puzzle/puzzle_game.py
```

If you are already inside the `family_puzzle` folder:

```bash
python3 puzzle_game.py
```

## How it works

- The game loads puzzles from `puzzles.json`.
- You get 5 random puzzles each round.
- You have 2 attempts per puzzle.
- If your first guess is wrong, you get a hint.

## Customize puzzles

Edit `family_puzzle/puzzles.json`.

Each puzzle object should have:

```json
{
  "type": "word",
  "prompt": "Puzzle text",
  "answer": "expected answer",
  "hint": "small clue",
  "explanation": "teaching explanation shown after missed puzzle"
}
```

Tips:
- Keep answers simple and kid-friendly.
- Use puzzle types like `word`, `math`, or `logic`.
- Add more puzzles to increase replay variety.
