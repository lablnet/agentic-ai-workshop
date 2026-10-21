"""A small agent that prepares a draft but cannot save it."""

from langchain.agents import create_agent

from prompts import DRAFT_PROMPT


def build_draft_agent(model):
    """
    Build the draft-only agent.

    Args:
        model: The model to use for the agent.

    Returns:
        An agent that writes announcements but has no save tools.
    """
    # Create the agent with no tools so it cannot write files on its own.
    return create_agent(model=model, tools=[], system_prompt=DRAFT_PROMPT)
