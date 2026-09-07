# Transcript -> Summary

# summarizer
# │
# ├── splitter
# ├── ollama
# ├── gemini
# ├── parser
# ├── chunk_prompt
# ├── final_prompt
# ├── chunk_chain
# └── final_chain

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

class TranscriptSummarizer:

    def __init__(self):

        # -----------------------------
        # Text Splitter
        # -----------------------------
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

        # -----------------------------
        # Ollama Model
        # -----------------------------
        self.ollama = ChatOllama(model="llama3.1:latest", temperature=0)

        # -----------------------------
        # Gemini Model
        # -----------------------------
        self.gemini = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2,
            google_api_key=os.getenv("GEMINI_API_KEY"),
        )

        # -----------------------------
        # Output Parser
        # -----------------------------
        self.parser = StrOutputParser()

        # -----------------------------
        # Prompt : Chunk Summary
        # -----------------------------
        self.chunk_prompt = PromptTemplate(
            template="""
                You are an expert transcript summarizer.

                Summarize ONLY this chunk.

                Rules:
                - Preserve important information.
                - Don't invent facts.
                - Keep it concise.

                Chunk:
                {chunk}
            """,
            input_variables=["chunk"],
        )

        # -----------------------------
        # Prompt : Final Summary
        # -----------------------------
        self.final_prompt = PromptTemplate(
            template="""
                You are an expert summarization assistant.

                Below are summaries generated from different transcript chunks.

                Create ONE final summary.

                Rules:
                - Remove duplicate information.
                - Keep logical flow.
                - Preserve important technical details.
                - Do not hallucinate.

                Chunk Summaries:

                {summaries}
            """,
            input_variables=["summaries"],
        )

        # -----------------------------
        # LangChain Pipelines
        # -----------------------------
        self.chunk_chain = self.chunk_prompt | self.ollama | self.parser
        self.final_chain = self.final_prompt | self.gemini | self.parser

    # ==================================================

    def summarize(self, transcript):

        # -----------------------------
        # Split Transcript
        # -----------------------------
        chunks = self.splitter.create_documents([transcript])

        # -----------------------------
        # Summarize Each Chunk
        # -----------------------------
        chunk_summaries = []

        for chunk in chunks:
            chunk_summary = self.chunk_chain.invoke({"chunk": chunk.page_content})
            chunk_summaries.append(chunk_summary)

        # -----------------------------
        # Merge Chunk Summaries
        # -----------------------------
        combined_summary = "\n\n".join(chunk_summaries)

        # -----------------------------
        # Final Gemini Summary
        # -----------------------------
        final_summary = self.final_chain.invoke({"summaries": combined_summary})

        return final_summary
