from meeting.graph import meeting_graph

audio_path = input("Enter audio file path: ")

state = {
    "audio_path": audio_path,
    "transcript": "",
    "summary": "",
    "tasks": []
}

result = meeting_graph.invoke(state)

print("\n===== TRANSCRIPT =====")
print(result["transcript"])

print("\n===== SUMMARY =====")
print(result["summary"])

print("\n===== TASKS =====")
print(result["tasks"])