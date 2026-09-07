# Text -> Summary
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from meeting.state import MeetingState

import os

load_dotenv()


class MeetingSummarizer:

    def __init__(self):

        # Text Splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=800, chunk_overlap=150
        )

        # Ollama
        self.ollama = ChatOllama(model="llama3.1:latest", temperature=0)

        # Gemini
        self.gemini = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2,
            google_api_key=os.getenv("GEMINI_API_KEY"),
        )

        # Output Parser
        self.parser = StrOutputParser()

        # Prompt for chunk summarization
        self.chunk_prompt = PromptTemplate(
            template="""
You are an expert meeting summarizer.

Summarize ONLY the following meeting chunk.

Focus on:
- Key discussion points
- Decisions made
- Important technical details

Ignore:
- Greetings
- Small talk
- Jokes
- Repeated information

Meeting Chunk:
{chunk}
""",
            input_variables=["chunk"],
        )

        # Prompt for final summary
        self.final_prompt = PromptTemplate(
            template="""
You are an expert meeting assistant.

Below are summaries generated from different meeting chunks.

Create ONE final meeting summary.

Rules:

- Merge duplicate information.
- Keep the logical flow.
- Preserve important technical discussions.
- Preserve important decisions.
- Do not invent information.

Chunk Summaries:

{summaries}
""",
            input_variables=["summaries"],
        )

        # Chains
        self.chunk_chain = self.chunk_prompt | self.ollama | self.parser

        self.final_chain = self.final_prompt | self.gemini | self.parser

    def summarize(self, state: MeetingState):

        print("Generating Meeting Summary...")

        transcript = state["transcript"]

        # Split transcript
        chunks = self.splitter.create_documents([transcript])

        chunk_summaries = []

        # Summarize every chunk
        for chunk in chunks:

            summary = self.chunk_chain.invoke({"chunk": chunk.page_content})

            chunk_summaries.append(summary)

        # Combine summaries
        combined_summary = "\n\n".join(chunk_summaries)

        # Final Gemini summary
        final_summary = self.final_chain.invoke({"summaries": combined_summary})

        print("Meeting Summary Generated")

        return {"summary": final_summary}
