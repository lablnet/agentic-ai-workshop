"""Prepared event loop and routing around the live-coded LangGraph agent."""

import logging
import time

from agent import analyze_email, build_email_agent
from .gmail_client import list_incoming_ids, read_email
from tool import build_email_tools
from .models import validate_analysis
from .state import load_processed, save_processed


def process_email(service, model, owner, email, on_success=None):
    """
    Process an email.
    Args:
        service: The Gmail API service object.
        model: The model used to build an agent with this email's tools.
        owner: The owner of the email.
        email: The email object.
    """
    tools, action = build_email_tools(service, owner, email, on_success)
    agent = build_email_agent(model, tools)
    # The agent selects and invokes a Gmail tool; do not repeat its action here.
    analysis = analyze_email(agent, email)
    # Validate the analysis.
    validate_analysis(analysis)
    if action["receipt"] is None:
        raise RuntimeError("The agent finished without a successful Gmail action.")
    if analysis != action["analysis"]:
        raise RuntimeError("Final output differs from the completed action. Check Gmail; success was already recorded.")
    logging.info("SUMMARY | %s", analysis.summary)
    kind = "DRAFT" if analysis.needs_reply else "SELF-SUMMARY"
    logging.info("%s | %s", kind, action["receipt"]["id"])


def watch_inbox(service, model, owner, folder, interval):
    """
    Watch the inbox for new emails and process them.
    Args:
        service: The Gmail API service object.
        model: The model used for fresh, independent email agents.
        owner: The owner of the email.
        folder: The folder to save the processed emails.
        interval: The interval to check the inbox.
    """
    # Load the processed emails.
    state_path = folder / "processed.json"
    # If the state path exists, load the processed emails.
    if state_path.exists():
        # Load the processed emails.
        processed = load_processed(state_path)
    else:
        # Baseline existing test emails so only subsequent arrivals trigger actions.
        processed = set(list_incoming_ids(service))
        save_processed(state_path, processed)
        logging.info("STARTUP | skipped %s existing matching messages", len(processed))
    logging.info("WATCHING | send a fresh email with AI-DEMO in its subject")
    while True:
        # Gmail lists newest first; reversing handles older arrivals first.
        for gmail_id in reversed(list_incoming_ids(service)):
            if gmail_id in processed:
                continue
            email = read_email(service, gmail_id, owner)
            if email is not None:
                logging.info("NEW EMAIL | %s", gmail_id)
                def record_success(message_id=gmail_id):
                    processed.add(message_id)
                    save_processed(state_path, processed)

                process_email(service, model, owner, email, record_success)
            # Mark complete only after the Gmail action succeeded, or an own message was skipped.
            processed.add(gmail_id)
            save_processed(state_path, processed)
        time.sleep(interval)
