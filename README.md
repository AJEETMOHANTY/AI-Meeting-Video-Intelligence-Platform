# Allen — AI Meeting Video Intelligence Platform

Allen is an AI-powered knowledge platform that converts unstructured information
such as YouTube videos and meeting recordings into structured, searchable, and
actionable knowledge.

The platform currently supports two main modes:

- YouTube Intelligence
- Meeting Intelligence

Allen uses transcription, LLM-based summarization, task extraction, embeddings,
vector search, RAG, PostgreSQL, FastAPI, Streamlit, and LangGraph.

---

## What Problem Does Allen Solve?

Important information is often spread across long YouTube videos and meeting
recordings.

Manually watching an entire video or reviewing a long meeting transcript to find
specific information, decisions, or tasks is time-consuming.

Allen processes this information automatically and allows users to:

- Generate summaries
- Ask questions about the source
- Search information using RAG
- Extract actionable meeting tasks
- Assign task owners
- Change task status
- Add new tasks manually
- Edit existing tasks
- Delete unnecessary tasks
- Persist information in PostgreSQL

---

# Project Modes

## 1. YouTube Intelligence

The user provides a YouTube URL.

Allen:

1. Fetches the video transcript
2. Splits the transcript into chunks
3. Generates intermediate summaries using a local LLM
4. Generates the final summary using Gemini
5. Stores the video information in PostgreSQL
6. Creates embeddings
7. Stores vectors in FAISS
8. Allows the user to ask questions about the video

### YouTube Flow

YouTube URL
↓
Transcript Extraction
↓
Text Chunking
↓
Ollama
↓
Intermediate Summaries
↓
Gemini
↓
Final Summary
↓
PostgreSQL
↓
Embeddings
↓
FAISS
↓
RAG
↓
Chat with Video

The chat system retrieves relevant transcript chunks from FAISS and uses Gemini
to answer questions based only on the video content.

If the requested information is not present in the transcript, Allen does not
invent an answer.

---

# 2. Meeting Intelligence

The user uploads a meeting audio file.

Allen:

1. Transcribes the meeting using Whisper
2. Splits the transcript into chunks
3. Generates a meeting summary
4. Extracts actionable tasks
5. Identifies task owners when mentioned
6. Stores the meeting in PostgreSQL
7. Stores extracted tasks in PostgreSQL
8. Creates embeddings for the transcript
9. Uses FAISS for retrieval
10. Allows the user to chat with the meeting

### Meeting Flow

Meeting Audio
↓
Whisper
↓
Transcript
↓
┌───────────────────┐
│                   │
▼                   ▼
Summary          Task Extraction
│                   │
▼                   ▼
PostgreSQL       PostgreSQL
│
▼
Embeddings
↓
FAISS
↓
RAG
↓
Chat with Meeting

---

# Task Management

Allen does not only extract meeting tasks.

The manager can also manage the extracted tasks.

Each task contains:

- Task
- Owner
- Status

Supported statuses:

- Pending
- Completed

The manager can:

- Add a task
- Edit a task
- Change the owner
- Change the status
- Delete a task

Task changes are persisted in PostgreSQL.

---

# Architecture

Allen follows a layered architecture.

Streamlit
    ↓
FastAPI
    ↓
Application Processing
    ↓
PostgreSQL / FAISS / LLMs

### Frontend

Streamlit is currently used for the user interface.

It provides:

- YouTube URL input
- Meeting audio upload
- Summary display
- Task management
- RAG chat

### Backend

FastAPI provides the API layer between the frontend and the processing
components.

The frontend communicates with FastAPI instead of directly calling the
processing logic.

### Database

PostgreSQL stores persistent application data.

Current database entities include:

- YouTube
- Meeting
- Task

### Vector Store

FAISS is used for vector similarity search.

It allows Allen to retrieve relevant transcript sections before generating
answers.

### LLMs

Gemini is used for final summaries and RAG responses.

Ollama is used for local LLM processing such as intermediate summarization.

### Workflow Orchestration

LangGraph is used to orchestrate the meeting processing workflow.

Meeting processing currently follows:

START
↓
Whisper
↓
Summary
↓
Task Extraction
↓
END

---

# Project Structure

```text
Allen/
│
├── backend/
│   ├── __init__.py
│   └── main.py
│
├── database/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── crud.py
│   └── test_crud.py
│
├── youtube/
│   ├── youtube_transcript.py
│   ├── summary.py
│   ├── chat.py
│   └── processor.py
│
├── meeting/
│   ├── state.py
│   ├── whisper.py
│   ├── summary.py
│   ├── task_extractor.py
│   ├── graph.py
│   ├── chat.py
│   ├── processor.py
│   ├── test_graph.py
│   └── test_processor.py
│
├── app/
│   └── ...
│
├── main_meeting.py
├── .env
├── .gitignore
└── README.md
