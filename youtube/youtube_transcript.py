# YouTube URL -> Transcript

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter

class YouTubeTranscript:

    def get_transcript(self, url):
        video_id = self.extract_video_id(url)
        try:
            ytt_api = YouTubeTranscriptApi()

            transcript_data = ytt_api.fetch(video_id)

            transcript = " ".join(
                snippet.text for snippet in transcript_data.snippets
            )
            
            return transcript

        except TranscriptsDisabled:
            return "No captions available for this video."

    def extract_video_id(self, url):
        # Extract the video ID from the URL
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        else:
            raise ValueError("Invalid YouTube URL")
