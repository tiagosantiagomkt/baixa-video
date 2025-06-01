# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
import yt_dlp
import uuid
import os

app = FastAPI()

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class VideoRequest(BaseModel):
    url: str

@app.post("/baixar")
async def baixar_video(data: VideoRequest):
    video_id = str(uuid.uuid4())
    output_path = f"{DOWNLOAD_DIR}/{video_id}.%(ext)s"

    ydl_opts = {
        "outtmpl": output_path,
        "format": "bestvideo+bestaudio/best"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([data.url])
        return {"status": "ok", "id": video_id}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
