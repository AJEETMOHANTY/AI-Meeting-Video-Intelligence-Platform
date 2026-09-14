import requests
import streamlit as st
from youtube.chat import TranscriptChat
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

# ==============================
# YouTube
# ==============================
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

            # API Call to backend
            response = requests.post(
                "http://127.0.0.1:8000/youtube/process", params={"url": url}
            )
            response.raise_for_status()
            video = response.json()

            chat = TranscriptChat()
            chat.load_transcript(video["transcript"])

        st.session_state.video = video
        st.session_state.chat = chat
        st.session_state.messages = []

        st.success("Video processed successfully!")

# Show video information
if st.session_state.video:

    video = st.session_state.video

    st.write("### Title")
    st.write(video["title"])

    st.write("### Summary")
    st.write(video["summary"])


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

# ==============================
# Meeting
# =============================
st.subheader("🎙️ Meeting")

audio_file = st.file_uploader("Upload Meeting Audio", type=["mp3", "wav", "m4a"])

if st.button("Process Meeting"):

    if audio_file is None:
        st.warning("Please upload a meeting audio file")

    else:

        with st.spinner("Processing meeting..."):

            response = requests.post(
                "http://127.0.0.1:8000/meeting/process",
                files={
                    "audio_file": (
                        audio_file.name,
                        audio_file.getvalue(),
                        audio_file.type,
                    )
                },
            )

            response.raise_for_status()

            result = response.json()

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
    st.write(meeting["title"])

    st.write("### Summary")
    st.write(meeting["summary"])

    st.write("### Tasks")
    
    # Code for addition of new task.

    if "add_task" not in st.session_state:
        st.session_state.add_task = False

    if st.button("+ Add Task"):
        st.session_state.add_task = True

    if st.session_state.add_task:

        with st.form("add_task_form"):

            new_task = st.text_input(
                "Task"
            )

            new_owner = st.text_input(
                "Owner",
                value="Unknown"
            )

            new_status = st.selectbox(
                "Status",
                ["Pending", "Completed"]
            )

            submitted = st.form_submit_button("Add Task")

            if submitted:

                if not new_task.strip():
                    st.warning("Please enter a task.")

                else:

                    response = requests.post(
                        f"http://127.0.0.1:8000/meeting/{meeting['meeting_id']}/task",
                        params={
                            "task": new_task,
                            "owner": new_owner,
                            "status": new_status
                        }
                    )

                    response.raise_for_status()

                    created_task = response.json()

                    meeting["tasks"].append(created_task)

                    st.session_state.add_task = False

                    st.toast("Task added successfully!")

                    st.rerun()

    # Code for editing and deleting tasks.
    for i, task in enumerate(meeting["tasks"]):

        st.write(f"#### Task {i + 1}")

        edited_task = st.text_input("Task", value=task["task"], key=f"task_{task['id']}")

        edited_owner = st.text_input(
            "Owner", value=task["owner"], key=f"owner_{task['id']}"
        )

        edited_status = st.selectbox(
            "Status",
            ["Pending", "Completed"],
            index=0 if task["status"].lower() == "pending" else 1,
            key=f"status_{task['id']}",
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Save Changes", key=f"save_{task['id']}"):

                response = requests.put(
                    f"http://127.0.0.1:8000/task/{task['id']}",
                    params={
                        "task": edited_task,
                        "owner": edited_owner,
                        "status": edited_status,
                    },
                )

                response.raise_for_status()

                updated_task = response.json()

                task["task"] = updated_task["task"]
                task["owner"] = updated_task["owner"]
                task["status"] = updated_task["status"]

                st.success("Task updated successfully!")

        with col2:
            if st.button("Delete Task", key=f"delete_{task['id']}"):
                st.session_state[f"confirm_delete_{task['id']}"] = True

            if st.session_state.get(f"confirm_delete_{task['id']}", False):

                st.warning("Are you sure you want to delete this task?")

                confirm_col1, confirm_col2 = st.columns(2)

                with confirm_col1:
                    if st.button(
                        "Yes, Delete",
                        key=f"confirm_{task['id']}"
                    ):
                        response = requests.delete(
                            f"http://127.0.0.1:8000/task/{task['id']}"
                        )

                        response.raise_for_status()

                        meeting["tasks"].remove(task)

                        del st.session_state[f"confirm_delete_{task['id']}"]

                        st.success("Task deleted successfully!")

                with confirm_col2:
                    if st.button(
                        "Cancel",
                        key=f"cancel_{task['id']}"
                    ):
                        del st.session_state[f"confirm_delete_{task['id']}"]
                        st.rerun()

        st.divider()


# Meeting Chat
if st.session_state.meeting_chat:

    st.subheader("💬 Ask Allen about the Meeting")

    for message in st.session_state.meeting_messages:

        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.text_input("Ask a question about this meeting...")

    if st.button("Ask Meeting"):

        if question:

            st.session_state.meeting_messages.append(
                {"role": "user", "content": question}
            )

            with st.chat_message("user"):
                st.write(question)

            with st.chat_message("assistant"):

                with st.spinner("Allen is thinking..."):

                    answer = st.session_state.meeting_chat.ask(question)

                st.write(answer)

            st.session_state.meeting_messages.append(
                {"role": "assistant", "content": answer}
            )
