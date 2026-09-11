from meeting.processor import process_meeting


audio_path = "DS Staff Meeting.mp3"

result = process_meeting(audio_path)

print("\n===== MEETING =====")
print("ID:", result["meeting_id"])
print("Title:", result["meeting_title"])

print("\n===== TASKS =====")

for task in result["tasks"]:
    print(task)