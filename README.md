Asana Simulation — Seed Data Generator

Generates a realistic Asana-like SQLite database for a simulated enterprise organization.

Quick start

1. Install deps:

```bash
F:/2022BCD0028/final/.venv/Scripts/python.exe -m pip install -r requirements.txt
```

2. Run generator (defaults to 200 users for quick runs):

```bash
F:/2022BCD0028/final/.venv/Scripts/python.exe src/main.py --users 200
```

3. Output DB: `output/asana_simulation.sqlite`

Configuration

- `--users` controls number of users (supports up to 10000). Other sizes increase runtime and DB size.

Files of interest

- `schema.sql` — SQLite DDL
- `src/` — generator code
- `prompts/llm_prompts.md` — placeholder LLM prompts
