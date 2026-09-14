import os

from meeting.graph import meeting_graph
from database.database import SessionLocal
from database.crud import (
    create_meeting,
    create_task,
    get_meeting_by_title,
    get_tasks_by_meeting_id,
)


def process_meeting(audio_path):

    db = SessionLocal()

    title = os.path.splitext(os.path.basename(audio_path))[0]

    try:

        # -------------------------
        # Check duplicate meeting
        # -------------------------
        existing_meeting = get_meeting_by_title(db, title)

        if existing_meeting:

            print("Meeting already exists. Fetching from database...")

            tasks = get_tasks_by_meeting_id(db, existing_meeting.id)

            return {
                "meeting_id": existing_meeting.id,
                "meeting_title": existing_meeting.title,
                "transcript": existing_meeting.transcript,
                "summary": existing_meeting.summary,
                "tasks": [
                    {
                        "id": task.id,
                        "task": task.task,
                        "owner": task.owner,
                        "status": task.status,
                    }
                    for task in tasks
                ],
            }

        # -------------------------
        # Process new meeting
        # -------------------------
        print("Processing new meeting...")

        result = meeting_graph.invoke(
            {
                "audio_path": audio_path,
            }
        )

        transcript = result["transcript"]
        summary = result["summary"]
        tasks = result["tasks"]

        meeting = create_meeting(
            db=db,
            title=title,
            transcript=transcript,
            summary=summary,
        )

        print(f"Meeting saved with ID: {meeting.id}")

        saved_tasks = []

        for task in tasks:

            saved_task = create_task(
                db=db,
                meeting_id=meeting.id,
                task=task["task"],
                owner=task["owner"],
                status=task["status"],
            )

            saved_tasks.append(
                {
                    "id": saved_task.id,
                    "task": saved_task.task,
                    "owner": saved_task.owner,
                    "status": saved_task.status,
                }
            )

        print("Tasks saved successfully!")

        return {
            "meeting_id": meeting.id,
            "meeting_title": meeting.title,
            "transcript": transcript,
            "summary": summary,
            "tasks": saved_tasks,
        }

    finally:
        db.close()