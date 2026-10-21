"""Add conversation memory to a small LangGraph-backed agent."""

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from prompts import MEMORY_PROMPT


def build_memory_agent(model):
    return create_agent(
        model=model,
        tools=[],
        system_prompt=MEMORY_PROMPT,
        checkpointer=InMemorySaver(),
    )
