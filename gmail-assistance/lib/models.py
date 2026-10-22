"""The information passed into and returned by the live-coded agent."""

from pydantic import BaseModel, ConfigDict


class IncomingEmail(BaseModel):
    gmail_id: str
    thread_id: str
    sender: str
    reply_to: str
    subject: str
    body: str
    message_id: str
    references: str


class EmailAnalysis(BaseModel):
    model_config = ConfigDict(strict=True)
    summary: str
    needs_reply: bool
    draft_reply: str | None = None


def validate_analysis(analysis: EmailAnalysis) -> None:
    if not analysis.summary.strip():
        raise ValueError("The summary cannot be empty.")
    if analysis.needs_reply and not (analysis.draft_reply or "").strip():
        raise ValueError("A reply is needed, but the agent did not provide a draft.")
    if not analysis.needs_reply and analysis.draft_reply is not None:
        raise ValueError("Use draft_reply=null when no reply is needed.")
