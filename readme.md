dbagent/
├── __init__.py
├── config.py                  # env-based settings (LLM key, DB path, retries, server)
├── db.py                      # DB class – SQLite connect/schema/execute/close
├── main.py                    # FastAPI app – REST + WebSocket + static serving
├── agents/
│   ├── __init__.py
│   ├── base.py                # AbstractAgent (abstract process())
│   └── db_agent.py            # DBAgent – orchestrates skills, calls LLM, retry loop
├── skills/
│   ├── __init__.py
│   ├── base.py                # AbstractSkill (abstract execute())
│   ├── docs_skill.py          # DocsSkill – schema context & table descriptions
│   ├── sql_skill.py           # SQLSkill – validate, parse, sanitize, read-only check
│   └── data_skill.py          # DataSkill – run query, format results, handle errors
├── frontend/
│   └── index.html             # Dark-themed chat UI with WebSocket support
requirements.txt               # fastapi, uvicorn, pydantic