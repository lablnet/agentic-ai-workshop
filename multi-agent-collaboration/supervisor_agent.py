"""The supervisor uses specialist agents as its tools."""

from langchain.agents import create_agent

from prompts import SUPERVISOR_PROMPT


def build_supervisor_agent(model, agent_tools):
    return create_agent(
        model=model,
        tools=agent_tools,
        name="supervisor",
        system_prompt=SUPERVISOR_PROMPT,
    )
