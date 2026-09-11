# This file will become the bridge between Meeting AI + Database:

import os
from meeting.graph import meeting_graph
from database.database import SessionLocal
from database.crud import create_meeting, create_task

def process_meeting(audio_path):

    print("Processing Meeting...")

    # Run the Meeting AI pipeline
    result = meeting_graph.invoke(
        {
            "audio_path": audio_path
        }
    )

    transcript = result["transcript"]
    summary = result["summary"]
    tasks = result["tasks"]

    # Create database session
    db = SessionLocal()

    try:

        # Use audio filename as meeting title
        title = os.path.splitext(os.path.basename(audio_path))[0]

        # Save meeting
        meeting = create_meeting(
            db=db,
            title=title,
            transcript=transcript,
            summary=summary
        )

        print(f"Meeting saved with ID: {meeting.id}")

        # Save extracted tasks
        for task in tasks:

            create_task(
                db=db,
                meeting_id=meeting.id,
                task=task["task"],
                owner=task["owner"],
                status=task["status"]
            )

        print("Tasks saved successfully!")

        meeting_id = meeting.id
        meeting_title = meeting.title

        return {
            "meeting_id": meeting_id,
            "meeting_title": meeting_title,
            "transcript": transcript,
            "tasks": tasks
        }

    finally:
        db.close()