from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import yt_dlp
import os
import uuid
import shutil

app = FastAPI()
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/baixar")
async def baixar_video(
    url: str = Form(...),
    cookies: UploadFile = File(None)
):
    id = str(uuid.uuid4())
    output_path = f"{OUTPUT_DIR}/{id}.mp4"
    cookie_path = None

    try:
        ydl_opts = {
            "outtmpl": output_path
        }

        if cookies:
            cookie_path = f"/tmp/{id}_cookies.txt"
            with open(cookie_path, "wb") as f:
                shutil.copyfileobj(cookies.file, f)
            ydl_opts["cookiefile"] = cookie_path

        yt_dlp.YoutubeDL(ydl_opts).download([url])
        return {"status": "ok", "arquivo": f"/{output_path}"}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}
    finally:
        if cookie_path and os.path.exists(cookie_path):
            os.remove(cookie_path)
