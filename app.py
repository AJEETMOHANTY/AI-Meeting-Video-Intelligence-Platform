import streamlit as st
from youtube.chat import TranscriptChat
from youtube.processor import process_youtube
from meeting.processor import process_meeting
from meeting.chat import MeetingChat

# Session state
if "chat" not in st.session_state:
    st.session_state.chat = None

if "video" not in st.session_state:
    st.session_state.video = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "meeting" not in st.session_state:
    st.session_state.meeting = None

if "meeting_chat" not in st.session_state:
    st.session_state.meeting_chat = None

if "meeting_messages" not in st.session_state:
    st.session_state.meeting_messages = []


# Page setup
st.set_page_config(page_title="Allen", page_icon="🤖", layout="wide")


# Title
st.title("🤖 Allen - Unified Knowledge Platform")


# YouTube
st.subheader("🎥 YouTube")

url = st.text_input(
    "Enter YouTube URL", placeholder="https://www.youtube.com/watch?v=..."
)


# Process video
if st.button("Process Video"):

    if not url:
        st.warning("Please enter a YouTube URL")

    else:

        with st.spinner("Processing video..."):

            video = process_youtube(url)

            chat = TranscriptChat()
            chat.load_transcript(video.transcript)

        st.session_state.video = video
        st.session_state.chat = chat
        st.session_state.messages = []

        st.success("Video processed successfully!")

# Show video information
if st.session_state.video:

    video = st.session_state.video

    st.write("### Title")
    st.write(video.title)

    st.write("### Summary")
    st.write(video.summary)


# Chat
if st.session_state.chat:

    st.subheader("💬 Ask Allen")

    # Show previous messages
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    # New question
    question = st.chat_input("Ask something about this video...")

    if question:

        # Show user question
        st.session_state.messages.append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.write(question)

        # Get answer
        with st.chat_message("assistant"):

            with st.spinner("Allen is thinking..."):

                answer = st.session_state.chat.ask(question)

            st.write(answer)

        # Save answer
        st.session_state.messages.append({"role": "assistant", "content": answer})

# Meeting
st.subheader("🎙️ Meeting")

audio_file = st.file_uploader(
    "Upload Meeting Audio",
    type=["mp3", "wav", "m4a"]
)

if st.button("Process Meeting"):

    if audio_file is None:
        st.warning("Please upload a meeting audio file")

    else:

        with st.spinner("Processing meeting..."):

            audio_path = audio_file.name

            with open(audio_path, "wb") as f:
                f.write(audio_file.getbuffer())

            result = process_meeting(audio_path)

            chat = MeetingChat()
            chat.load_transcript(result["transcript"])

        st.session_state.meeting = result
        st.session_state.meeting_chat = chat
        st.session_state.meeting_messages = []

        st.success("Meeting processed successfully!")


# Show Meeting information
if st.session_state.meeting:

    meeting = st.session_state.meeting

    st.write("### Meeting Title")
    st.write(meeting["meeting_title"])

    st.write("### Summary")
    st.write(meeting["summary"])

    st.write("### Tasks")

    for task in meeting["tasks"]:

        st.write(
            f"- {task['task']} | "
            f"Owner: {task['owner']} | "
            f"Status: {task['status']}"
        )


# Meeting Chat
if st.session_state.meeting_chat:

    st.subheader("💬 Ask Allen about the Meeting")

    for message in st.session_state.meeting_messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.text_input(
        "Ask a question about this meeting..."
    )

    if st.button("Ask Meeting"):

        if question:

            st.session_state.meeting_messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):

                with st.spinner("Allen is thinking..."):

                    answer = st.session_state.meeting_chat.ask(
                        question
                    )

                st.write(answer)

            st.session_state.meeting_messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )