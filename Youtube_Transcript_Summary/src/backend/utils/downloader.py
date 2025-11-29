from yt_dlp import YoutubeDL
import os
import hashlib

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def _video_id_from_url(url: str) -> str:
    # fallback: hash if no id
    h = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
    return h

def download_audio(url: str) -> str:
    """
    Downloads audio to downloads/<videoid>.mp3 and returns path.
    If already exists, returns existing path.
    """
    try:
        # try get id using yt-dlp info
        ydl_opts = {"quiet": True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            vid = info.get("id") or _video_id_from_url(url)
    except Exception:
        vid = _video_id_from_url(url)

    out = os.path.join(DOWNLOAD_DIR, f"{vid}.mp3")
    if os.path.exists(out):
        return out

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out,
        "quiet": True,
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
        ],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return out