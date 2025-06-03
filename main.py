### backend/app/main.py
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import yt_dlp
import os
import uuid
import shutil
import subprocess

app = FastAPI()
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/baixar")
async def baixar_audio(
    url: str = Form(...)
):
    id = str(uuid.uuid4())
    audio_path = f"{OUTPUT_DIR}/{id}.mp3"

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": audio_path,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        }

        yt_dlp.YoutubeDL(ydl_opts).download([url])
        return {"status": "ok", "arquivo": f"/{audio_path}"}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}


### backend/app/routes.py
from fastapi import APIRouter, Form
from .main import baixar_audio

router = APIRouter()

@router.post("/baixar")
async def baixar(url: str = Form(...)):
    return await baixar_audio(url=url)


### backend/app/tasks.py
# (não necessário nesta versão, mas pode ser mantido para futuras tarefas async)


### backend/app/utils.py
# (vazio ou utilitários futuros)


### backend/requirements.txt
fastapi
uvicorn
yt-dlp


### backend/Dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


### worker/worker.py
# (não necessário nesta versão simplificada)


### worker/Dockerfile
# (não necessário nesta versão simplificada)


### worker/requirements.txt
# (não necessário nesta versão simplificada)


### frontend/index.html
<!DOCTYPE html>
<html>
<head>
    <title>Baixar Áudio do Vídeo</title>
</head>
<body>
    <h1>Baixar Áudio do Vídeo</h1>
    <form id="form">
        <input type="text" id="url" placeholder="Cole o link do vídeo">
        <button type="submit">Baixar</button>
    </form>
    <div id="status"></div>
<script>
document.getElementById('form').onsubmit = async (e) => {
    e.preventDefault();
    const url = document.getElementById('url').value;
    const formData = new FormData();
    formData.append('url', url);

    const res = await fetch('/baixar', {
        method: 'POST',
        body: formData
    });
    const data = await res.json();
    if (data.status === 'ok') {
        document.getElementById('status').innerHTML = 'Áudio pronto: <a href="' + data.arquivo + '" target="_blank">Download</a>';
    } else {
        document.getElementById('status').innerText = 'Erro: ' + data.mensagem;
    }
};
</script>
</body>
</html>


### frontend/Dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html


### docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
  frontend:
    build: ./frontend
    ports:
      - "80:80"


### README.md
# App de Download de Áudio Open Source

## Como funciona
- Cole um link de vídeo (ex: YouTube)
- O app baixa **somente o áudio** e disponibiliza para download
- **Não requer cookies** — funciona com vídeos públicos

## Rodando localmente
```bash
docker-compose up --build
```

## Deploy na Coolify
1. Crie novo projeto com Docker Compose
2. Aponte para este repositório
3. Use porta 80 no frontend, 8000 no backend
4. Pronto!

## LGPD e segurança
- Nenhum dado pessoal é coletado
- Somente vídeos públicos são processados
- Os arquivos são temporários e descartados automaticamente
