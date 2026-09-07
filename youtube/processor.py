from database.database import SessionLocal
from database.crud import get_youtube_by_url, save_youtube
from youtube.youtube_transcript import YouTubeTranscript
from youtube.summary import TranscriptSummarizer
import requests


def get_youtube_title(url):
    response = requests.get(
        "https://www.youtube.com/oembed", params={"url": url, "format": "json"}
    )

    response.raise_for_status()

    return response.json()["title"]


def process_youtube(url):
    print("Processing YouTube video...")

    db = SessionLocal()
    existing_video = get_youtube_by_url(db, url)

    if existing_video:
        print("Video already exists in database!")

        youtube_record = existing_video
        transcript = existing_video.transcript
        summary = existing_video.summary

    else:
        print("New video. Processing...")
        print("Fetching transcript...")

        youtube = YouTubeTranscript()
        transcript = youtube.get_transcript(url)

        print("Transcript fetcheds successfully!")
        print("Generating summary...")

        summarizer = TranscriptSummarizer()
        summary = summarizer.summarize(transcript)

        print("Summary generated!")
        print("Getting YouTube title...")

        title = get_youtube_title(url)

        print("Title fetched!")

        youtube_record = save_youtube(
            db=db, title=title, url=url, transcript=transcript, summary=summary
        )

    db.close()

    return youtube_record
