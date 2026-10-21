"""The supervisor uses specialist agents as its tools."""

from langchain.agents import create_agent

from prompts import SUPERVISOR_PROMPT


def build_supervisor_agent(model, agent_tools):
    # Create the agent
    # The create_agent function creates an agent that can use the tools provided.
    return create_agent(
        model=model,
        tools=agent_tools,
        name="supervisor",
        system_prompt=SUPERVISOR_PROMPT,
    )
