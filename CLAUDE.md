# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
pip install fastapi uvicorn openai
export OPENAI_API_KEY=sk-...
```

## Running the server

```bash
python hello.py
```

Server starts on `http://localhost:8000`. Interactive API docs at `http://localhost:8000/docs`.

## Architecture

Single-file FastAPI app (`hello.py`) with one endpoint:

- `GET /resources?topic=<topic>` — calls OpenAI `gpt-4o-mini` with a structured prompt, parses the JSON response, and returns it validated through Pydantic models.

**Data flow:** query param → f-string prompt → OpenAI `json_object` response → `json.loads` → Pydantic `ResourcesResponse` → JSON response.

**Models:**
- `Resources` — the nested object with `books`, `courses`, `websites`, `youtube` (all `list[str]`), and `tips` (str)
- `ResourcesResponse` — top-level with `topic: str` and `resources: Resources`

The OpenAI client is initialized at module level from `OPENAI_API_KEY` env var (hard fails on startup if missing).

## Git Workflow

This repo is on GitHub: `https://github.com/nhossa/pathwaygen`

**Commit on important changes** to preserve progress and prevent losing work:
- After implementing a new feature
- After fixing a bug
- After significant refactoring
- After making infrastructure/config changes

**Common commit patterns:**
```bash
# After feature implementation
git add .
git commit -m "Add feature: description of what was added"

# After bug fix
git add .
git commit -m "Fix: description of bug that was fixed"

# After refactoring
git add .
git commit -m "Refactor: description of code changes"

# Push to GitHub
git push origin master
```

**Environment file:** `.env` is gitignored (never pushed). Each developer creates their own locally.
