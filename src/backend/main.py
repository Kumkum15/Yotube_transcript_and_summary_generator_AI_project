from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.youtube_meta import get_youtube_metadata
from utils.downloader import download_audio
from utils.transcript import generate_transcript
from utils.summaries import generate_summary

app = FastAPI(title="YouTube Transcript & Summary API (Local models)")

# Allow frontend to call backend (dev only)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

@app.post("/validate")
def validate(req: URLRequest):
    try:
        meta = get_youtube_metadata(req.url)
        if not meta:
            raise HTTPException(status_code=400, detail="Unable to fetch metadata")
        return {"status": "valid", "meta": meta}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/download")
def download(req: URLRequest):
    try:
        path = download_audio(req.url)
        return {"status": "downloaded", "audio_path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribe")
def transcribe(req: URLRequest):
    try:
        audio_path = download_audio(req.url)
        text = generate_transcript(audio_path)
        return {"status": "transcribed", "transcript": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
def summarize(req: URLRequest):
    try:
        audio_path = download_audio(req.url)
        text = generate_transcript(audio_path)
        summary = generate_summary(text)
        return {"status": "summarized", "summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))