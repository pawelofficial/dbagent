from __future__ import annotations

import hashlib
import hmac
import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from dbagent.config import (
    AUTH_USERNAME, AUTH_PASSWORD, AUTH_SECRET,
    DB_PATH, HOST, PORT,
)

app = FastAPI(title="DBAgent", version="0.1.0")

FRONTEND_DIR = Path(__file__).parent / "frontend"


# ------------------------------------------------------------------
# In-memory stores (replace with DB-backed storage later)
# ------------------------------------------------------------------

_chats: dict[str, dict[str, Any]] = {}  # chat_id -> {title, created_at, messages}


def _get_or_create_chat(chat_id: str | None) -> tuple[str, dict[str, Any]]:
    if chat_id and chat_id in _chats:
        return chat_id, _chats[chat_id]
    new_id = uuid.uuid4().hex[:12]
    _chats[new_id] = {
        "title": "New chat",
        "created_at": datetime.utcnow().isoformat(),
        "messages": [],
    }
    return new_id, _chats[new_id]


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
    result = []
    for cid, chat in sorted(_chats.items(), key=lambda x: x[1]["created_at"], reverse=True):
        result.append({
            "id": cid,
            "title": chat["title"],
            "created_at": chat["created_at"],
            "message_count": len(chat["messages"]),
        })
    return JSONResponse(result)


@app.get("/api/chats/{chat_id}")
async def get_chat(chat_id: str, username: str = Depends(_require_auth)) -> JSONResponse:
    if chat_id not in _chats:
        raise HTTPException(status_code=404, detail="Chat not found")
    return JSONResponse({"id": chat_id, **_chats[chat_id]})


# ------------------------------------------------------------------
# Query endpoint — returns "noted" for now
# ------------------------------------------------------------------

@app.post("/api/query", response_model=QueryResponse)
async def query(req: QueryRequest, username: str = Depends(_require_auth)) -> QueryResponse:
    chat_id, chat = _get_or_create_chat(req.chat_id)

    chat["messages"].append({
        "role": "user",
        "content": req.question,
        "timestamp": datetime.utcnow().isoformat(),
    })

    if chat["title"] == "New chat":
        chat["title"] = req.question[:50]

    answer = "noted"

    chat["messages"].append({
        "role": "agent",
        "content": answer,
        "timestamp": datetime.utcnow().isoformat(),
    })

    return QueryResponse(answer=answer, chat_id=chat_id)


@app.get("/api/schema")
async def schema(username: str = Depends(_require_auth)) -> JSONResponse:
    raise NotImplementedError


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

            chat_id, chat = _get_or_create_chat(chat_id_in)

            chat["messages"].append({
                "role": "user",
                "content": question,
                "timestamp": datetime.utcnow().isoformat(),
            })
            if chat["title"] == "New chat":
                chat["title"] = question[:50]

            answer = "noted"

            chat["messages"].append({
                "role": "agent",
                "content": answer,
                "timestamp": datetime.utcnow().isoformat(),
            })

            await ws.send_json({
                "step": "done",
                "chat_id": chat_id,
                "payload": {"answer": answer},
            })
    except WebSocketDisconnect:
        pass


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
