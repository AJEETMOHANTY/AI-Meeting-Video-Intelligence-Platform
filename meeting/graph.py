from langgraph.graph import StateGraph, START, END
from meeting.state import MeetingState
from meeting.whisper import WhisperTranscriber
from meeting.summary import MeetingSummarizer
from meeting.task_extractor import TaskExtractor

# Create Objects
whisper = WhisperTranscriber()
summarizer = MeetingSummarizer()
task_extractor = TaskExtractor()

# Create Graph
graph = StateGraph(MeetingState)

# Add Nodes
graph.add_node("whisper", whisper.whisper_node)  #  ,transcribe
graph.add_node("summary", summarizer.summarize)
graph.add_node("tasks", task_extractor.extract_tasks)

# Connect Nodes
graph.add_edge(START, "whisper")
graph.add_edge("whisper", "summary")
graph.add_edge("whisper", "tasks")
graph.add_edge("summary", END)
graph.add_edge("tasks", END)

# Compile Graph
meeting_graph = graph.compile()
