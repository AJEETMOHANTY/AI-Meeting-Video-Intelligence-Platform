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
from dotenv import load_dotenv
import os
from langchain_core.runnables import (
    RunnableParallel,
    RunnableLambda,
    RunnablePassthrough,
)

load_dotenv()


class TranscriptChat:

    def __init__(self):

        # Splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
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
            You are a helpful assistant.

            Answer ONLY from the provided transcript context.

            If the context does not contain enough information to answer the question,
            respond exactly with: "I don't know."

            Context:
            {context}

            Question:
            {question}
            """,
            input_variables=["context", "question"],
        )

        # Parser
        self.parser = StrOutputParser()

        # These will be created later
        self.vector_store = None
        self.retriever = None

    def load_transcript(self, transcript):
        chunks = self.splitter.create_documents([transcript])
        self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": 4}
        )

    def format_docs(self, retrieved_docs):
        return "\n\n".join(doc.page_content for doc in retrieved_docs)

    def ask(self, question):
        parallel_chain = RunnableParallel(
            {
                "context": self.retriever | RunnableLambda(self.format_docs),
                "question": RunnablePassthrough(),
            }
        )

        main_chain = parallel_chain | self.prompt | self.llm | self.parser
        answer = main_chain.invoke(question)
        return answer
