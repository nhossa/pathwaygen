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
