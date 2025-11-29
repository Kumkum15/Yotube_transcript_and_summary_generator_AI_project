from transformers import pipeline
import textwrap

_summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0 if __import__("torch").cuda.is_available() else -1)

def _chunk_text(text, max_chars=1500):
    # naive chunker by sentences/characters
    paragraphs = text.split("\n")
    buf = ""
    for p in paragraphs:
        if len(buf) + len(p) + 1 > max_chars:
            yield buf
            buf = p
        else:
            buf = buf + "\n" + p if buf else p
    if buf:
        yield buf

def generate_summary(transcript: str) -> str:
    if not transcript or len(transcript.strip()) == 0:
        return "No transcript to summarize."

    chunks = list(_chunk_text(transcript, max_chars=1500))
    summaries = []
    for c in chunks:
        # the pipeline returns a list of dicts
        out = _summarizer(c, max_length=200, min_length=40, do_sample=False)
        summaries.append(out[0]["summary_text"])
    # join chunk summaries, then optionally summarize again if too long
    joined = " ".join(summaries)
    if len(joined) > 500:
        final = _summarizer(joined, max_length=300, min_length=80, do_sample=False)[0]["summary_text"]
        return final
    return joined