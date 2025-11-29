
1. YouTube Video Transcript and Summary Generator

Developer:
Name: Kumkum Hirani
Email: kumkumhirani.co@gmail.com

2. Project Overview

A full-stack application where a user can:

a. Validate YouTube URL
b. Download audio
c. Generate transcript 
d. Generate summary 
e. Fetch video metadata

3. Tech Stack

Backend: FastAPI, yt-dlp, Whisper (OpenAI Tiny), Transformers
Frontend: HTML, CSS, JavaScript
Others: Torch, NumPy

4. Folder Structure

Youtube_Transcript_Summary/
   src/
      backend/
      frontend/
   screenshots/
   README.md

5. Setup Instructions

A. Backend Setup

cd src/backend

python -m venv .venv

.\.venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload --host 127.0.0.1 --port 8000

Backend runs at:
> http://127.0.0.1:8000

B. Frontend Setup

cd src/frontend

python -m http.server 3000

Frontend runs at:
> http://127.0.0.1:3000

6. How to Use

Paste YouTube link

Click Validate
Choose a feature:

- Download Audio
- Generate Transcript
- Generate Summary
- Fetch Metadata

View all results LIVE on UI

7. Screenshots Included

Placed inside /screenshots/:

YouTube URL input

Validation success

Transcript generated

Summary generated

Metadata fetched


# AI_Project
This project helps in converting youtube video to transcript and summary. It can also give meta data and even download audio just by pasting the URL. 

