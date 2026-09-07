# Audio/Video -> Text

from langgraph.graph import StateGraph, START, END
from faster_whisper import WhisperModel
from meeting.state import MeetingState


class WhisperTranscriber:

    def __init__(self):

        # Load Whisper model only once
        self.model = WhisperModel("base", device="cpu", compute_type="int8")

    def whisper_node(self, state: MeetingState):

        print("Transcribing Audio...")

        audio_path = state["audio_path"]

        # Transcribe audio
        segments, info = self.model.transcribe(audio_path)

        transcript = ""

        # Combine all segments
        for segment in segments:
            transcript += segment.text + " "

        print("Transcription Completed")

        return {"transcript": transcript}
