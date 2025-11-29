import os
from openai import OpenAI

def _get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment")
    return OpenAI(api_key=api_key)

def generate_transcript(audio_path: str) -> str:
    """
    Uses OpenAI new SDK to call audio transcription.
    Returns plain text transcript.
    """
    client = _get_client()
    with open(audio_path, "rb") as f:
        # model name may change; this uses a current compatible model name
        resp = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=f
        )
    # `resp.text` is expected for transcription response
    return getattr(resp, "text", None) or resp.get("text") or str(resp)