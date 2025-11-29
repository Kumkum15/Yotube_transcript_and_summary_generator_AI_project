import os
from openai import OpenAI

def _get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment")
    return OpenAI(api_key=api_key)

def generate_summary(transcript_text: str) -> dict:
    """
    Returns a dict with: short_summary, bullets, key_insights, action_items
    """
    client = _get_client()

    system = "You are an assistant. Produce a clear short summary (100-150 words), bullets, key insights, and action items from the transcript."
    user = f"Transcript:\n{transcript_text}"

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=0.2,
        max_tokens=800
    )

    content = resp.choices[0].message.content
    # The model will return a text; we will return it raw plus attempt simple split for bullets
    return {"raw": content}