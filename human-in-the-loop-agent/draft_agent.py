"""A small agent that prepares a draft but cannot save it."""

from langchain.agents import create_agent

from prompts import DRAFT_PROMPT


def build_draft_agent(model):
    return create_agent(model=model, tools=[], system_prompt=DRAFT_PROMPT)
