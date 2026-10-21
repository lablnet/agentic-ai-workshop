"""The weather specialist has one job and one tool."""

from langchain.agents import create_agent

from prompts import WEATHER_PROMPT
from tools.main import get_weather


def build_weather_agent(model):
    # Create the agent
    # The create_agent function creates an agent that can use the tools provided.
    return create_agent(
        model=model,
        tools=[get_weather],
        name="weather_agent",
        system_prompt=WEATHER_PROMPT,
    )
