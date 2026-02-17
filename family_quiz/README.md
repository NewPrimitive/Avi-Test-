# Family Quiz Game (Starter Scaffold)

A beginner-friendly terminal quiz game for a parent and child to build together.

## Quick start (from repository root)
Run this command from the repository root folder (`/workspace/Avi-Test-`):

```bash
python3 family_quiz/quiz.py
```

If you are already inside the `family_quiz` folder, run:

```bash
python3 quiz.py
```

## What you'll learn
- Variables and data types
- Loops and conditionals
- Functions
- Reading/writing JSON files
- Basic program structure

## Customize questions
Edit `family_quiz/questions.json`.

Each question looks like:

```json
{
  "question": "Your question text",
  "choices": ["Choice 1", "Choice 2", "Choice 3", "Choice 4"],
  "answer": 2,
  "explanation": "Optional teaching explanation"
}
```

Notes:
- `answer` is **1-based** (1 means first choice).
- Keep at least 2 choices per question.

## Stretch goals
- Add difficulty levels (`easy`, `medium`, `hard`)
- Add a timer per question
- Track streaks for correct answers
- Let players choose categories
- Build a web version with HTML/CSS/JavaScript
