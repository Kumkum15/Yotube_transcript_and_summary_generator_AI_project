import librosa
import soundfile as sf
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import os

processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)


def generate_transcript(audio_path: str) -> str:
    try:
        # Step 1 → Load audio at original sampling rate (usually 44100)
        audio, sr = librosa.load(audio_path, sr=None)

        # Step 2 → Resample audio → 16000 Hz (required by Whisper)
        audio_16k = librosa.resample(audio, orig_sr=sr, target_sr=16000)

        # Step 3 → Save temporary resampled audio
        temp_path = audio_path.replace(".mp3", "_16k.wav")
        sf.write(temp_path, audio_16k, 16000)

        # Step 4 → Process through Whisper
        inputs = processor(audio_16k, sampling_rate=16000, return_tensors="pt")
        input_features = inputs.input_features.to(device)

        predicted_ids = model.generate(input_features)
        text = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

        return text

    except Exception as e:
        return f"Transcript generation failed: {str(e)}"