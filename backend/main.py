from fastapi import FastAPI
from youtube.processor import process_youtube
from meeting.processor import process_meeting
from fastapi import FastAPI, UploadFile, File

app = FastAPI(title="Allen API")

@app.get("/")
def home():
    return {"message": "Allen API is running"}


@app.post("/youtube/process")
def process_video(url: str):

    video = process_youtube(url)

    return {
        "id": video.id,
        "title": video.title,
        "url": video.url,
        "transcript": video.transcript,
        "summary": video.summary,
    }


@app.post("/meeting/process")
async def process_meeting_api(audio_file: UploadFile = File(...)):

    audio_path = audio_file.filename

    with open(audio_path, "wb") as file:
        file.write(await audio_file.read())

    result = process_meeting(audio_path)

    return {
        "meeting_id": result["meeting_id"],
        "title": result["meeting_title"],
        "summary": result["summary"],
        "tasks": result["tasks"]
    }