from meeting.graph import meeting_graph
from meeting.chat import MeetingChat


def main():

    audio_path = "DS Staff Meeting.mp3"

    print("Processing Meeting...\n")

    # Run LangGraph
    result = meeting_graph.invoke(
        {
            "audio_path": audio_path
        }
    )

    print("\nMeeting Summary")
    print("=" * 50)
    print(result["summary"])

    print("\nExtracted Tasks")
    print("=" * 50)

    for task in result["tasks"]:
        print(task)

    # -------------------------------
    # Meeting Chat
    # -------------------------------

    chat = MeetingChat()

    chat.load_transcript(result["transcript"])

    print("\nMeeting Chat Started")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You : ")

        if question.lower() == "exit":
            break

        answer = chat.ask(question)

        print("\nAssistant :")
        print(answer)
        print()


if __name__ == "__main__":
    main()