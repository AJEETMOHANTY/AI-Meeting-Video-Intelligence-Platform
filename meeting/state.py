from typing import TypedDict

class MeetingState(TypedDict):
    audio_path: str
    transcript: str
    summary: str
    tasks: list
    