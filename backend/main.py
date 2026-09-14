from fastapi import FastAPI, UploadFile, File
from youtube.processor import process_youtube
from meeting.processor import process_meeting
from database.database import SessionLocal
from database.crud import create_task, update_task, delete_task

app = FastAPI(title="Allen API")


@app.get("/")
def home():
    return {"message": "Allen API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


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
        "transcript": result["transcript"],
        "summary": result["summary"],
        "tasks": result["tasks"],
    }


@app.post("/meeting/{meeting_id}/task")
def create_task_api(
    meeting_id: int,
    task: str,
    owner: str,
    status: str = "Pending"
):
    db = SessionLocal()

    new_task = create_task(
        db=db,
        meeting_id=meeting_id,
        task=task,
        owner=owner,
        status=status
    )

    db.close()

    return {
        "id": new_task.id,
        "task": new_task.task,
        "owner": new_task.owner,
        "status": new_task.status
    }
    
    
@app.put("/task/{task_id}")
def update_task_api(
    task_id: int,
    task: str,
    owner: str,
    status: str
):
    db = SessionLocal()

    updated_task = update_task(
        db=db,
        task_id=task_id,
        task=task,
        owner=owner,
        status=status
    )

    db.close()

    if updated_task is None:
        return {"error": "Task not found"}

    return {
        "id": updated_task.id,
        "task": updated_task.task,
        "owner": updated_task.owner,
        "status": updated_task.status
    }
    
    
@app.delete("/task/{task_id}")
def delete_task_api(task_id: int):
    db = SessionLocal()

    result = delete_task(
        db=db,
        task_id=task_id
    )

    db.close()

    if result is None:
        return {"error": "Task not found"}

    return {
        "message": "Task deleted successfully"
    }