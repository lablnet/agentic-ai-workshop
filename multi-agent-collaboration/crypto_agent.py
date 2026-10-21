"""The crypto specialist has one job and one tool."""

from langchain.agents import create_agent

from prompts import CRYPTO_PROMPT
from tools.main import get_crypto_price


def build_crypto_agent(model):
    # Create the agent
    # The create_agent function creates an agent that can use the tools provided.
    return create_agent(
        model=model,
        tools=[get_crypto_price],
        name="crypto_agent",
        system_prompt=CRYPTO_PROMPT,
    )
