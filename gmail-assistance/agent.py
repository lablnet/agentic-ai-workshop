"""Working email agent; marked blocks can be removed before live coding."""

import json

from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

from lib.models import EmailAnalysis, IncomingEmail
from prompt import EMAIL_PROMPT


def build_email_agent(model, tools):
    """Build a LangGraph-backed agent that summarizes emails and drafts replies."""
    # TODO BEFORE LIVE CODING: remove this implementation and rebuild it on stage.
    # BEGIN LIVE-CODING BLOCK
    return create_agent(
        model=model,
        tools=tools,
        system_prompt=EMAIL_PROMPT,
        response_format=ToolStrategy(EmailAnalysis),
    )
    # END LIVE-CODING BLOCK
    # lib/watcher.py creates the tools for the current email via build_email_tools().
    # The model chooses create_reply_draft or send_summary_to_self.
    # Credentials, recipient addresses and the original email are bound in Python;
    # the model supplies only summary/reply text. Tool inputs are validated first.
    # ToolStrategy returns the typed answer under result["structured_response"].


def analyze_email(agent, email: IncomingEmail) -> EmailAnalysis:
    """Let the agent choose a Gmail tool, then return its structured result."""
    content = json.dumps({"sender": email.sender, "subject": email.subject, "body": email.body})
    # TODO BEFORE LIVE CODING: remove this implementation and write it on stage.
    # BEGIN LIVE-CODING BLOCK
    result = agent.invoke(
        {"messages": [{"role": "user", "content": content}]},
        config={"recursion_limit": 12},
    )
    return EmailAnalysis.model_validate(result["structured_response"])
    # END LIVE-CODING BLOCK
    # No credentials, Gmail service object, or earlier emails go into the prompt.


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
