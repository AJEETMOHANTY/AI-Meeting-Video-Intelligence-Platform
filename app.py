import streamlit as st
from youtube.chat import TranscriptChat
from youtube.processor import process_youtube

# Session state
if "chat" not in st.session_state:
    st.session_state.chat = None

if "video" not in st.session_state:
    st.session_state.video = None

if "messages" not in st.session_state:
    st.session_state.messages = []


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
