# Lily Quiz Game

A terminal quiz game featuring **KATSEYE trivia** and fun prompts inspired by the movie **K-Pop Demon Hunters**.

## Quick start (from repository root)

```bash
python3 lily_quiz/quiz.py
```

## What's inside
- 10 total questions
- Multiple-choice answers
- Instant feedback for each question
- High score tracking in `lily_quiz/highscores.json`

## Customize questions
Edit `lily_quiz/questions.json`.

Question format:

```json
{
  "question": "Question text",
  "choices": ["Choice 1", "Choice 2", "Choice 3", "Choice 4"],
  "answer": 1,
  "explanation": "Why that answer is correct"
}
```

Notes:
- `answer` is 1-based (1 means the first choice).
- Keep at least 2 choices for each question.
