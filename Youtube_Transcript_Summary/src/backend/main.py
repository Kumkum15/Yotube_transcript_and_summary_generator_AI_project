from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import traceback

# load env BEFORE anything else that needs OPENAI_API_KEY
load_dotenv()

from utils.youtube_meta import get_youtube_metadata
from utils.downloader import download_audio
from utils.transcript import generate_transcript
from utils.summaries import generate_summary

app = FastAPI(title="YouTube Transcript & Summary API")

# allow frontend (for dev only, be restrictive in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

@app.post("/validate")
def validate(req: URLRequest):
    meta = get_youtube_metadata(req.url)
    if meta is None or meta.get("error"):
        raise HTTPException(status_code=400, detail=meta.get("error", "Invalid URL"))
    return {"status": "valid", "meta": meta}

@app.post("/download")
def download(req: URLRequest):
    try:
        audio_path = download_audio(req.url)
        return {"status": "downloaded", "audio_path": audio_path}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transcribe")
def transcribe(req: URLRequest):
    try:
        # reuse downloader -> ensures file exists
        audio_path = download_audio(req.url)
        transcript = generate_transcript(audio_path)
        return {"status": "transcribed", "transcript": transcript}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
def summarize(req: URLRequest):
    try:
        # if user sends url, generate transcript first
        audio_path = download_audio(req.url)
        transcript = generate_transcript(audio_path)
        summary = generate_summary(transcript)
        return {"status": "summarized", "summary": summary}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))