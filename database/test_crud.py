# ==========================
# CREATE
# ==========================
# from database.database import SessionLocal
# from database.crud import save_youtube

# db = SessionLocal()

# youtube = save_youtube(
#     db=db,
#     title="LangGraph Tutorial",
#     url="https://youtube.com/test",
#     transcript="This is a sample transcript.",
#     summary="This is a sample summary."
# )

# print(youtube.id)
# print(youtube.title)

# db.close()

# ==========================
# READ
# ==========================
# from database.database import SessionLocal
# from database.crud import get_youtube_by_id

# db = SessionLocal()

# youtube = get_youtube_by_id(
#     db=db,
#     youtube_id=1
# )

# print(youtube)
# print("ID:", youtube.id)
# print("Title:", youtube.title)
# print("URL:", youtube.url)
# print("Transcript:", youtube.transcript)
# print("Summary:", youtube.summary)
# print("Created At:", youtube.created_at)

# db.close()

# =========================
# UPDATE
# =========================
# from database.database import SessionLocal

# from database.crud import update_youtube

# db = SessionLocal()

# youtube = update_youtube(db=db, youtube_id=1, title="LangGraph Complete Course")

# print("ID:", youtube.id)
# print("Title:", youtube.title)

# db.close()

# ==========================
# DELETE
# ==========================
# from database.database import SessionLocal
# from database.crud import delete_youtube

# db = SessionLocal()

# result = delete_youtube(db=db, youtube_id=1)

# print(result)

# db.close()

# ===========================
# READ ALL RECORDS
# ===========================
# from database.database import SessionLocal
# from database.crud import save_youtube, get_all_youtube

# db = SessionLocal()

# save_youtube(
#     db=db,
#     title="Video 1",
#     url="https://youtube.com/1",
#     transcript="Transcript 1",
#     summary="Summary 1"
# )

# save_youtube(
#     db=db,
#     title="Video 2",
#     url="https://youtube.com/2",
#     transcript="Transcript 2",
#     summary="Summary 2"
# )

# videos = get_all_youtube(db)

# for video in videos:
#     print(video.id, video.title)

# db.close()

# ===========================
# COUNT RECORDS
# ===========================
# from database.database import SessionLocal
# from database.crud import count_youtube

# db = SessionLocal()

# count = count_youtube(db)

# print("Total Videos:", count)

# db.close()

# ===========================
# GET YOUTUBE BY TITLE
# ===========================
# from database.database import SessionLocal
# from database.crud import get_youtube_by_title

# db = SessionLocal()

# video = get_youtube_by_title(
#     db=db,
#     title="Video 1"
# )

# if video:
#     print("ID:", video.id)
#     print("Title:", video.title)
#     print("URL:", video.url)
# else:
#     print("Video not found")

# db.close()

# ===========================
# CREATE MEETING
# ===========================
# from database.database import SessionLocal
# from database.crud import create_meeting

# db = SessionLocal()

# meeting = create_meeting(
#     db=db,
#     title="Team Project Meeting",
#     transcript="We discussed the backend and frontend development.",
#     summary="The team discussed the project development."
# )

# print("Meeting Created!")
# print("ID:", meeting.id)
# print("Title:", meeting.title)
# print("Summary:", meeting.summary)

# db.close()

# ==========================
# GET MEETING BY ID
# ==========================
# from database.database import SessionLocal
# from database.crud import get_meeting_by_id

# db = SessionLocal()

# meeting = get_meeting_by_id(db, 1)

# if meeting:
#     print("ID:", meeting.id)
#     print("Title:", meeting.title)
#     print("Transcript:", meeting.transcript)
#     print("Summary:", meeting.summary)
# else:
#     print("Meeting not found")

# db.close()

# ==========================
# GET ALL MEETINGS
# ==========================
# from database.database import SessionLocal
# from database.crud import get_all_meetings

# db = SessionLocal()

# meetings = get_all_meetings(db)

# for meeting in meetings:
#     print("ID:", meeting.id)
#     print("Title:", meeting.title)
#     print("-" * 30)

# db.close()

# ==========================
# COUNT MEETINGS
# ==========================
# from database.database import SessionLocal
# from database.crud import count_meetings

# db = SessionLocal()

# count = count_meetings(db)

# print("Total Meetings:", count)

# db.close()

# ==========================
# UPDATE MEETING
# ==========================
# from database.database import SessionLocal
# from database.crud import update_meeting

# db = SessionLocal()

# meeting = update_meeting(
#     db=db,
#     meeting_id=1,
#     title="Updated Team Meeting"
# )

# if meeting:
#     print("ID:", meeting.id)
#     print("Title:", meeting.title)
# else:
#     print("Meeting not found")

# db.close()

# ==========================
# DELETE MEETING
# ==========================
# from database.database import SessionLocal
# from database.crud import delete_meeting

# db = SessionLocal()

# result = delete_meeting(
#     db=db,
#     meeting_id=1
# )

# print("Delete Result:", result)

# db.close()

# ==========================
# CREATE TASK
# ==========================
# from database.database import SessionLocal
# from database.crud import create_task

# db = SessionLocal()

# new_task = create_task(
#     db=db,
#     meeting_id=2,
#     task="Build the backend API",
#     owner="Ajeet",
#     status="Pending"
# )

# print("Task Created!")
# print("ID:", new_task.id)
# print("Meeting ID:", new_task.meeting_id)
# print("Task:", new_task.task)
# print("Owner:", new_task.owner)
# print("Status:", new_task.status)

# db.close()

# ==========================
# GET TASK BY ID
# ==========================
# from database.database import SessionLocal
# from database.crud import get_task_by_id

# db = SessionLocal()

# task = get_task_by_id(db, 3)

# if task:
#     print("ID:", task.id)
#     print("Meeting ID:", task.meeting_id)
#     print("Task:", task.task)
#     print("Owner:", task.owner)
#     print("Status:", task.status)
# else:
#     print("Task not found")

# db.close()

# ==========================
# GET ALL TASKS
# ==========================
# from database.database import SessionLocal
# from database.crud import get_all_tasks

# db = SessionLocal()

# tasks = get_all_tasks(db)

# for task in tasks:
#     print("ID:", task.id)
#     print("Meeting ID:", task.meeting_id)
#     print("Task:", task.task)
#     print("Owner:", task.owner)
#     print("Status:", task.status)
#     print("-" * 30)

# db.close()

# ==========================
# COUNT TASKS
# ==========================
# from database.database import SessionLocal
# from database.crud import count_tasks

# db = SessionLocal()

# count = count_tasks(db)

# print("Total Tasks:", count)

# db.close()

# ==========================
# UPDATE TASK
# ==========================
# from database.database import SessionLocal
# from database.crud import update_task

# db = SessionLocal()

# task = update_task(
#     db=db,
#     task_id=6,
#     task="Build the FastAPI backend",
#     owner="Ajeet",
#     status="Completed"
# )

# if task:
#     print("ID:", task.id)
#     print("Task:", task.task)
#     print("Owner:", task.owner)
#     print("Status:", task.status)
# else:
#     print("Task not found")

# db.close()

# ==========================
# DELETE TASK
# ==========================
from database.database import SessionLocal
from database.crud import delete_task

db = SessionLocal()

result = delete_task(
    db=db,
    task_id=7
)

print("Delete Result:", result)

db.close()

# ==========================
# CREATE A MEETING -> TASKS
# ==========================
# from database.database import SessionLocal
# from database.models import Meeting, Task

# db = SessionLocal()

# # Create a meeting
# meeting = Meeting(
#     title="Allen Project Meeting",
#     transcript="We discussed backend and frontend.",
#     summary="Backend and frontend development."
# )

# # Create tasks
# task1 = Task(
#     task="Build FastAPI backend",
#     owner="Ajeet",
#     status="Pending"
# )

# task2 = Task(
#     task="Build Streamlit UI",
#     owner="Ajeet",
#     status="Pending"
# )

# # Connect tasks to the meeting
# meeting.tasks.append(task1)
# meeting.tasks.append(task2)

# db.add(meeting)
# db.commit()
# db.refresh(meeting)

# print("Meeting ID:", meeting.id)

# for task in meeting.tasks:
#     print(
#         "Task:",
#         task.task,
#         "| Owner:",
#         task.owner,
#         "| Status:",
#         task.status
#     )

# db.close()

# ==========================
# CREATE A TASKS -> MEETING
# ==========================
# from database.database import SessionLocal
# from database.models import Task

# db = SessionLocal()

# task = db.query(Task).filter(Task.task == "Build FastAPI backend").first()

# if task:
#     print("Task:", task.task)
#     print("Task ID:", task.id)
#     print("Meeting ID:", task.meeting_id)
#     print("Meeting Title:", task.meeting.title)
# else:
#     print("Task not found")

# db.close()
