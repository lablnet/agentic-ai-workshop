"""Add conversation memory to a small LangGraph-backed agent."""

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
# https://github.com/lablnet/langgraph-checkpoint-mongodb
# MongoDb checkpointer in typescript.


from prompts import MEMORY_PROMPT


def build_memory_agent(model):
    """
    Build the memory agent.

    Args:
        model: The model to use for the agent.

    Returns:
        The memory agent.
    """
    # Create the agent
    # The create_agent function creates an agent that can use the tools provided.
    # The checkpointer is the memory of the agent.
    return create_agent(
        model=model,
        tools=[],
        system_prompt=MEMORY_PROMPT,
        checkpointer=InMemorySaver(),
    )
