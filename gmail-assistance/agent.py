"""Working email agent; marked blocks can be removed before live coding."""

import json

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from lib.models import EmailAnalysis, IncomingEmail
from prompt import EMAIL_PROMPT


def build_email_agent(model, tools):
    """Build a LangGraph-backed agent that summarizes emails and drafts replies."""
    # TODO
    return create_agent(
        model=model,
        tools=tools,
        system_prompt=EMAIL_PROMPT,
        response_format=ToolStrategy(EmailAnalysis),
    )


def analyze_email(agent, email: IncomingEmail) -> EmailAnalysis:
    """Let the agent choose a Gmail tool, then return its structured result."""
    content = json.dumps({"sender": email.sender, "subject": email.subject, "body": email.body})
    # TODO
    result = agent.invoke(
        {"messages": [{"role": "user", "content": content}]},
        config={"recursion_limit": 12},
    )
    return EmailAnalysis.model_validate(result["structured_response"])


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run main.py for the assistant, or auth.py for login.")
    parser.add_argument("--auth-only", action="store_true")
    args = parser.parse_args()
    if args.auth_only:
        from auth import main
        main()
    else:
        parser.error("Run python3 gmail-assistance/main.py to start the assistant.")
