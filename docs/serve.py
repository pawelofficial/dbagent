from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

DIAGRAMS_DIR = Path(__file__).parent / "diagrams"

app = FastAPI()


@app.get("/")
def index():
    html = (Path(__file__).parent / "architecture.html").read_text(encoding="utf-8")
    return HTMLResponse(html)


@app.get("/api/diagrams")
def list_diagrams():
    return sorted(p.stem for p in DIAGRAMS_DIR.glob("*.mmd"))


@app.get("/api/diagrams/{name}")
def get_diagram(name: str):
    # Block path traversal
    if "/" in name or "\\" in name or ".." in name:
        raise HTTPException(403, "Forbidden")
    path = DIAGRAMS_DIR / f"{name}.mmd"
    if not path.is_file():
        raise HTTPException(404, "Not found")
    return FileResponse(path, media_type="text/plain")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=3000)
