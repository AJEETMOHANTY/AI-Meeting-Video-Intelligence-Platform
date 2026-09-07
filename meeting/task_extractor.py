import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from meeting.state import MeetingState

load_dotenv()


class TaskExtractor:

    def __init__(self):

        # Gemini LLM
        self.gemini = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=os.getenv("GEMINI_API_KEY"),
        )

        # JSON Parser
        self.parser = JsonOutputParser()

        # Prompt
        self.prompt = PromptTemplate(
            template="""
            You are an AI Meeting Assistant.

            Your job is to extract ONLY actionable tasks from the meeting transcript.

            Rules:

            - Return ONLY valid JSON.
            - Do not include markdown.
            - Ignore greetings, jokes and casual conversation.
            - Every task must have:
                - task
                - owner
                - status
            - If owner is not mentioned, write "Unknown".
            - Status should always be "pending".

            Output Format:

            {{
                "tasks":[
                    {{
                        "task":"...",
                        "owner":"...",
                        "status":"pending"
                    }}
                ]
            }}

            Meeting Transcript:

            {transcript}
            """,
            input_variables=["transcript"],
        )

        # Chain
        self.chain = self.prompt | self.gemini | self.parser

    def extract_tasks(self, state: MeetingState):

        print("Extracting Tasks...")
        transcript = state["transcript"]
        result = self.chain.invoke({"transcript": transcript})
        print("Task Extraction Completed")
        return {"tasks": result["tasks"]}
