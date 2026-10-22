"""Create plain-function tools bound to one email and the authenticated account."""

from threading import Lock

from lib.gmail_actions import create_reply_draft as save_draft
from lib.gmail_actions import send_summary_to_self as send_summary
from lib.models import EmailAnalysis, validate_analysis


def build_email_tools(service, owner, email, on_success=None):
    # These values stay in Python closures; they are not model tool arguments.
    action = {"attempted": False, "analysis": None, "receipt": None}
    lock = Lock()

    def execute(analysis):
        validate_analysis(analysis)
        # A model may request multiple tools in parallel. Permit just one Gmail action.
        with lock:
            if action["attempted"]:
                return "A Gmail action was already attempted. Do not call another action tool."
            action["attempted"] = True
            if analysis.needs_reply:
                receipt = save_draft(service, owner, email, analysis.draft_reply)
            else:
                receipt = send_summary(service, owner, email, analysis.summary)
            action["analysis"] = analysis
            action["receipt"] = receipt
            # Record success before returning to the model, which could fail afterward.
            if on_success:
                on_success()
            return f"Gmail action succeeded. ID: {receipt['id']}. Return the same summary and reply decision as your final structured answer."

    def create_reply_draft(summary: str, reply: str) -> str:
        """When a response is needed, summarize the email and save a reply as a Gmail draft. Does not send the reply."""
        return execute(EmailAnalysis(summary=summary, needs_reply=True, draft_reply=reply))

    def send_summary_to_self(summary: str) -> str:
        """When no response is needed, email a short summary only to the account owner."""
        return execute(EmailAnalysis(summary=summary, needs_reply=False, draft_reply=None))

    return [create_reply_draft, send_summary_to_self], action
