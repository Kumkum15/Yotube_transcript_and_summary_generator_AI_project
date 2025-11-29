import os
import yt_dlp

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_audio(url: str) -> str:
    # outtmpl uses ID and extension; then we convert to mp3 via ffmpeg postprocessor
    opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)

    audio_path = os.path.join(DOWNLOAD_DIR, f"{info['id']}.mp3")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Downloaded audio not found at {audio_path}")
    return audio_path
