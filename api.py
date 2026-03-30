from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()


class RenderRequest(BaseModel):
    order_id: str
    photos: list[str]
    phrases: list[str]


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/render")
def render_video(data: RenderRequest):
    print("🎬 Generando video para:", data.order_id)

    subprocess.run(
        ["python", "video_engine.py", data.order_id],
        check=True
    )

    return {
        "status": "rendering_started",
        "order_id": data.order_id
    }