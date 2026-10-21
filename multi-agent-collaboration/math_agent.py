"""The maths specialist has one job and one tool."""

from langchain.agents import create_agent

from prompts import MATH_PROMPT
from tools.main import calculate


def build_math_agent(model):
    # Create the agent
    # The create_agent function creates an agent that can use the tools provided.
    return create_agent(
        model=model,
        tools=[calculate],
        name="math_agent",
        system_prompt=MATH_PROMPT,
    )
