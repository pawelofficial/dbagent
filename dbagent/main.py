from __future__ import annotations

import hashlib
import hmac
import json
import time
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from dbagent.config import (
    AUTH_USERNAME, AUTH_PASSWORD, AUTH_SECRET,
    CHAT_DB_PATH, DB_PATH, HOST, PORT,
)
from dbagent.chat_store import ChatStore
from dbagent.db import DB

app = FastAPI(title="DBAgent", version="0.1.0")

FRONTEND_DIR = Path(__file__).parent / "frontend"

_store = ChatStore(CHAT_DB_PATH)
_db = DB(db_path=DB_PATH)


# ------------------------------------------------------------------
# Auth helpers — simple HMAC token
# ------------------------------------------------------------------

def _make_token(username: str) -> str:
    payload = f"{username}:{int(time.time())}"
    sig = hmac.new(AUTH_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{sig}"


def _verify_token(token: str) -> str | None:
    """Return username if valid, else None."""
    parts = token.split(":")
    if len(parts) != 3:
        return None
    username, _ts, sig = parts
    expected = hmac.new(AUTH_SECRET.encode(), f"{username}:{_ts}".encode(), hashlib.sha256).hexdigest()
    if hmac.compare_digest(sig, expected):
        return username
    return None


def _require_auth(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    username = _verify_token(auth[7:])
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username


# ------------------------------------------------------------------
# Request / response models
# ------------------------------------------------------------------

class LoginRequest(BaseModel):
    username: str
    password: str


class QueryRequest(BaseModel):
    question: str
    chat_id: str | None = None


class QueryResponse(BaseModel):
    answer: str
    chat_id: str
    sql: str | None = None
    data: dict | None = None
    error: str | None = None


# ------------------------------------------------------------------
# Auth endpoint
# ------------------------------------------------------------------

@app.post("/api/login")
async def login(req: LoginRequest) -> JSONResponse:
    if req.username == AUTH_USERNAME and req.password == AUTH_PASSWORD:
        token = _make_token(req.username)
        return JSONResponse({"token": token, "username": req.username})
    raise HTTPException(status_code=401, detail="Invalid credentials")


# ------------------------------------------------------------------
# Chat history endpoints
# ------------------------------------------------------------------

@app.get("/api/chats")
async def list_chats(username: str = Depends(_require_auth)) -> JSONResponse:
    return JSONResponse(_store.list_chats())


@app.get("/api/chats/{chat_id}")
async def get_chat(chat_id: str, username: str = Depends(_require_auth)) -> JSONResponse:
    chat = _store.get_chat(chat_id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return JSONResponse(chat)


# ------------------------------------------------------------------
# Query endpoint — returns "noted" for now
# ------------------------------------------------------------------

@app.post("/api/query", response_model=QueryResponse)
async def query(req: QueryRequest, username: str = Depends(_require_auth)) -> QueryResponse:
    if req.chat_id and _store.chat_exists(req.chat_id):
        chat_id = req.chat_id
    else:
        chat_id = _store.create_chat(title=req.question[:50])

    now = datetime.utcnow().isoformat()
    _store.add_message(chat_id, "user", req.question, now)

    answer = "noted"

    _store.add_message(chat_id, "agent", answer)

    return QueryResponse(answer=answer, chat_id=chat_id)


@app.get("/api/schema")
async def schema(username: str = Depends(_require_auth)) -> JSONResponse:
    return JSONResponse(_db.get_schema())


# ------------------------------------------------------------------
# WebSocket endpoint
# ------------------------------------------------------------------

@app.websocket("/ws/query")
async def ws_query(ws: WebSocket) -> None:
    await ws.accept()

    token_msg = await ws.receive_text()
    try:
        data = json.loads(token_msg)
        username = _verify_token(data.get("token", ""))
    except Exception:
        username = None

    if not username:
        await ws.send_json({"error": "unauthorized"})
        await ws.close(code=4001)
        return

    try:
        while True:
            raw = await ws.receive_text()
            data = json.loads(raw)
            question = data.get("question", "")
            chat_id_in = data.get("chat_id")

            if chat_id_in and _store.chat_exists(chat_id_in):
                chat_id = chat_id_in
            else:
                chat_id = _store.create_chat(title=question[:50])

            now = datetime.utcnow().isoformat()
            _store.add_message(chat_id, "user", question, now)

            answer = "noted"

            _store.add_message(chat_id, "agent", answer)

            await ws.send_json({
                "step": "done",
                "chat_id": chat_id,
                "payload": {"answer": answer},
            })
    except WebSocketDisconnect:
        pass


# ------------------------------------------------------------------
# Lifecycle
# ------------------------------------------------------------------

@app.on_event("shutdown")
async def shutdown() -> None:
    _store.close()
    _db.close()


# ------------------------------------------------------------------
# Frontend
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
