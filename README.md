# Trade API + MCP Server

A backend REST API for trade data built with FastAPI and SQLite, 
with an MCP (Model Context Protocol) server that connects Claude 
to query trade data conversationally.

## Tech Stack
- Python
- FastAPI
- SQLite + SQLAlchemy
- Anthropic MCP

## Features
- REST API with GET and POST endpoints for trade data
- Persistent storage via SQLite database
- MCP server allowing Claude to query trade data via natural language

## Setup
1. Clone the repo
2. Create a virtual environment: `python -m venv .venv`
3. Activate it: `source .venv/Scripts/activate` (Windows/Git Bash)
4. Install dependencies: `pip install fastapi uvicorn`
5. Run the API: `uvicorn main:app --reload`
6. Visit `http://localhost:8000/docs` to explore the API

## Endpoints
- `GET /trades` — returns all trades
- `GET /trades/{symbol}` — returns trades for a specific symbol
- `POST /trades` — adds a new trade