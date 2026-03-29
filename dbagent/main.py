from __future__ import annotations

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

from dbagent.db import DB
from dbagent.agents.db_agent import DBAgent
from dbagent.config import DB_PATH, HOST, PORT

app = FastAPI(title="DBAgent", version="0.1.0")

_db = DB(db_path=DB_PATH)
_agent = DBAgent(db=_db)

FRONTEND_DIR = Path(__file__).parent / "frontend"


# ------------------------------------------------------------------
# Request / response models
# ------------------------------------------------------------------

class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sql: str | None = None
    data: dict | None = None
    error: str | None = None


# ------------------------------------------------------------------
# REST endpoints
# ------------------------------------------------------------------

@app.post("/api/query", response_model=QueryResponse)
async def query(req: QueryRequest) -> QueryResponse:
    """Accept a natural-language question and return the agent's response."""
    raise NotImplementedError


@app.get("/api/schema")
async def schema() -> JSONResponse:
    """Return the full database schema."""
    raise NotImplementedError


# ------------------------------------------------------------------
# WebSocket endpoint
# ------------------------------------------------------------------

@app.websocket("/ws/query")
async def ws_query(ws: WebSocket) -> None:
    """Stream agent steps (docs, sql, data) over a WebSocket.

    Protocol (JSON messages)::

        Client -> {"question": "..."}
        Server -> {"step": "docs",  "payload": ...}
        Server -> {"step": "sql",   "payload": ...}
        Server -> {"step": "data",  "payload": ...}
        Server -> {"step": "done",  "payload": ...}
    """
    raise NotImplementedError


# ------------------------------------------------------------------
# Frontend static files
# ------------------------------------------------------------------

@app.get("/")
async def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")


app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


# ------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------

def main() -> None:
    import uvicorn
    uvicorn.run("dbagent.main:app", host=HOST, port=PORT, reload=True)


if __name__ == "__main__":
    main()
