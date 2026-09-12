# Only database operations.
from sqlalchemy.orm import Session  # Used to talk to PostgreSQL.
from database.models import YouTube, Meeting, Task

# ==========================
# ==========================
# YouTube CRUD
# ==========================
# ==========================


# ==========================
# SAVE DETAILS
# ==========================
def save_youtube(db: Session, title: str, url: str, transcript: str, summary: str):
    youtube = YouTube(title=title, url=url, transcript=transcript, summary=summary)

    db.add(youtube)
    db.commit()
    db.refresh(youtube)

    return youtube


# ==========================
# GET ALL YOUTUBE VIDEOS
# ==========================
def get_all_youtube(db: Session):
    return db.query(YouTube).all()


# ==========================
# GET YOUTUBE BY URL
# ==========================
def get_youtube_by_url(db: Session, url: str):
    return db.query(YouTube).filter(YouTube.url == url).first()


# ==========================
# GET YOUTUBE BY ID
# ==========================
def get_youtube_by_id(db: Session, youtube_id: int):
    return db.query(YouTube).filter(YouTube.id == youtube_id).first()


# db.query(YouTube) -> Read from the youtube table.
# .filter(YouTube.id == youtube_id) -> Adds a condition to the query.
# .first() -> Return only the first matching row.


# ==========================
# UPDATE
# ==========================
def update_youtube(db: Session, youtube_id: int, title: str):
    youtube = get_youtube_by_id(db, youtube_id)

    if youtube is None:
        return None

    youtube.title = title

    db.commit()
    db.refresh(youtube)

    return youtube


# ==========================
# DELETE
# ==========================
def delete_youtube(db: Session, youtube_id: int):
    youtube = get_youtube_by_id(db, youtube_id)

    if youtube is None:
        return None

    db.delete(youtube)
    db.commit()

    return True


# ===========================
# COUNT RECORDS
# ===========================
def count_youtube(db: Session):
    return db.query(YouTube).count()


# ===========================
# GET YOUTUBE BY TITLE
# ===========================
def get_youtube_by_title(db: Session, title: str):
    return db.query(YouTube).filter(YouTube.title == title).first()


# ==========================
# ==========================
# Meeting CRUD
# ==========================
# ==========================
# create_meeting()
#       ↓
# get_meeting_by_id()
#       ↓
# get_all_meetings()
#       ↓
# count_meetings()
#       ↓
# update_meeting()
#       ↓
# delete_meeting()


# ==========================
# CREATE MEETING
# ==========================
def create_meeting(db: Session, title: str, transcript: str, summary: str):
    meeting = Meeting(title=title, transcript=transcript, summary=summary)

    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    return meeting


# ==========================
# GET MEETING BY ID
# ==========================
def get_meeting_by_id(db: Session, meeting_id: int):
    return db.query(Meeting).filter(Meeting.id == meeting_id).first()


# ==========================
# GET ALL MEETINGS
# ==========================
def get_all_meetings(db: Session):
    return db.query(Meeting).all()


# ==========================
# COUNT MEETINGS
# ==========================
def count_meetings(db: Session):
    return db.query(Meeting).count()


# ==========================
# UPDATE MEETING
# ==========================
def update_meeting(db: Session, meeting_id: int, title: str):
    meeting = get_meeting_by_id(db, meeting_id)

    if meeting is None:
        return None

    meeting.title = title

    db.commit()
    db.refresh(meeting)

    return meeting


# ==========================
# DELETE MEETING
# ==========================
def delete_meeting(db: Session, meeting_id: int):
    meeting = get_meeting_by_id(db, meeting_id)

    if meeting is None:
        return None

    db.delete(meeting)
    db.commit()

    return True


# ==========================
# ==========================
# Task CRUD
# ==========================
# ==========================


# ==========================
# CREATE TASK
# ==========================
def create_task(
    db: Session, meeting_id: int, task: str, owner: str, status: str = "Pending"
):
    new_task = Task(meeting_id=meeting_id, task=task, owner=owner, status=status)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# ==========================
# GET TASK BY ID
# ==========================
def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


# ==========================
# GET ALL TASKS
# ==========================
def get_all_tasks(db: Session):
    return db.query(Task).all()


# ==========================
# COUNT TASKS
# ==========================
def count_tasks(db: Session):
    return db.query(Task).count()


# ==========================
# UPDATE TASK
# ==========================
def update_task(db: Session, task_id: int, status: str):
    task = get_task_by_id(db, task_id)

    if task is None:
        return None

    task.status = status

    db.commit()
    db.refresh(task)

    return task


# ==========================
# DELETE TASK
# ==========================
def delete_task(db: Session, task_id: int):
    task = get_task_by_id(db, task_id)

    if task is None:
        return None

    db.delete(task)
    db.commit()

    return True


# Add a duplicate check in database/crud.py
# ==========================
# GET MEETING BY TITLE
# ==========================
def get_meeting_by_title(db: Session, title: str):
    return db.query(Meeting).filter(Meeting.title == title).first()


# ==========================
# GET TASKS OF A MEETING
# ==========================
def get_tasks_by_meeting_id(db: Session, meeting_id: int):
    return db.query(Task).filter(Task.meeting_id == meeting_id).all()
