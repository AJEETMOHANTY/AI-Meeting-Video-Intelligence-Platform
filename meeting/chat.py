# Question -> Answer

# Transcript
#      ▼
# Text Splitter
#      ▼
# Embeddings
#      ▼
# FAISS
#      ▼
# Retriever
#      ▼
# Prompt
#      ▼
# Gemini
#      ▼
# Answer


from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableParallel,
    RunnableLambda,
    RunnablePassthrough,
)
from dotenv import load_dotenv

import os

load_dotenv()


class MeetingChat:

    def __init__(self):

        # Text Splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
        )

        # Embedding Model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-large-en-v1.5",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        # Gemini
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2,
            google_api_key=os.getenv("GEMINI_API_KEY"),
        )

        # Prompt
        self.prompt = PromptTemplate(
            template="""
You are an AI Meeting Assistant.

Answer the user's question ONLY using the provided meeting transcript.

Rules:

- Use ONLY the meeting transcript.
- Do NOT use outside knowledge.
- If the answer is not mentioned in the transcript, reply:
  "This information was not discussed in the meeting."
- Keep the answer concise and professional.
- If asked about:
    • tasks
    • owners
    • deadlines
    • decisions
    • action items
    • discussions

  answer only from the transcript.

Meeting Transcript:

{context}

Question:

{question}
""",
            input_variables=["context", "question"],
        )

        # Output Parser
        self.parser = StrOutputParser()

        # These will be initialized later
        self.vector_store = None
        self.retriever = None
        self.parallel_chain = None
        self.main_chain = None

    def load_transcript(self, transcript):

        # Split Transcript
        chunks = self.splitter.create_documents([transcript])

        # Create Vector Store
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)

        # Create Retriever
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4},
        )

        # Helper Function
        self.parallel_chain = RunnableParallel(
            {
                "context": self.retriever | RunnableLambda(self.format_docs),
                "question": RunnablePassthrough(),
            }
        )

        # Final Chain
        self.main_chain = self.parallel_chain | self.prompt | self.llm | self.parser

    def format_docs(self, retrieved_docs):

        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    def ask(self, question):

        if self.retriever is None:
            raise Exception("Please load the meeting transcript first.")

        answer = self.main_chain.invoke(question)

        return answer
