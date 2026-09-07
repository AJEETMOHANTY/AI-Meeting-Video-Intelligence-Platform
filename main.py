from ollama import chat
from youtube.youtube_transcript import YouTubeTranscript
from youtube.summary import TranscriptSummarizer
from youtube_transcript_api import YouTubeTranscriptApi
from youtube.chat import TranscriptChat
import requests

from meeting.graph import meeting_graph

from database.database import SessionLocal
from database.crud import save_youtube, get_youtube_by_url, get_all_youtube


def get_youtube_title(url):
    response = requests.get(
        "https://www.youtube.com/oembed", params={"url": url, "format": "json"}
    )

    response.raise_for_status()

    data = response.json()

    return data["title"]


def main():

    try:

        # url = "https://youtu.be/LPZh9BOjkQs?si=5psscag1qSk_nEAK"
        url = input("Enter YouTube URL: ")

        db = SessionLocal()

        existing_video = get_youtube_by_url(db, url)

        if existing_video:
            print("Video already exists in database!")
            youtube_record = existing_video
            transcript = existing_video.transcript
            summary = existing_video.summary

        else:
            print("Fetching transcript...")

            youtube = YouTubeTranscript()
            transcript = youtube.get_transcript(url)

            print("Transcript fetched successfully.\n")

            print("Generating summary...")

            summarizer = TranscriptSummarizer()
            summary = summarizer.summarize(transcript)

            title = get_youtube_title(url)

            youtube_record = save_youtube(
                db=db, title=title, url=url, transcript=transcript, summary=summary
            )

            print("Saved to PostgreSQL!")

        print("YouTube ID:", youtube_record.id)

        print("\nSaved YouTube Videos")
        print("=" * 40)

        videos = get_all_youtube(db)

        for video in videos:
            print(f"ID: {video.id}")
            print(f"Title: {video.title}")
            print(f"URL: {video.url}")
            print("-" * 40)

        db.close()

        # ---------- Chat ----------

        chat = TranscriptChat()
        chat.load_transcript(transcript)

        print("\nYouTube Chat Started")
        print("Type 'exit' to quit.\n")

        while True:

            question = input("You : ")

            if question.lower() == "exit":
                break

            answer = chat.ask(question)

            print("\nAllen :")
            print(answer)
            print("=" * 60)
        # ----------------------------

        print("\nFinal Summary")
        print("=" * 50)
        print(summary)

    except Exception as e:

        print(f"Error : {e}")


if __name__ == "__main__":

    main()
