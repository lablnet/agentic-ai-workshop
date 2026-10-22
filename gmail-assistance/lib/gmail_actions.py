"""Low-level Gmail operations used by the bound agent tools."""

from email.message import EmailMessage

from .gmail_client import encode_message


def _normalize_subject(subject: str) -> str:
    return subject.replace("\r", " ").replace("\n", " ")


def _make_message(owner: str, to: str, subject: str, body: str, **headers: str) -> EmailMessage:
    message = EmailMessage()
    message["From"] = owner
    message["To"] = to
    message["Subject"] = subject
    for key, value in headers.items():
        message[key] = value
    message.set_content(body)
    return message


def create_reply_draft(service, owner, email, reply):
    """
    Create a draft reply message for an email.
    Args:
        service: The Gmail API service object.
        owner: The owner of the email.
        email: The email object.
        reply: The reply message.
    Returns:
        The draft message.
    """
    if not email.reply_to or "@" not in email.reply_to:
        raise ValueError("The original email has no usable reply address.")

    subject = _normalize_subject(email.subject)
    reply_subject = subject if subject.lower().startswith("re:") else "Re: " + subject
    headers = {}
    if email.message_id:
        headers["In-Reply-To"] = email.message_id
        headers["References"] = (email.references + " " + email.message_id).strip()
    message = _make_message(owner, email.reply_to, reply_subject, reply, **headers)
    draft = {"message": {"raw": encode_message(message)}}
    if email.message_id:
        draft["message"]["threadId"] = email.thread_id
    # This creates a draft only. There is no drafts.send call in this application.
    return service.users().drafts().create(userId="me", body=draft).execute()


def send_summary_to_self(service, owner, email, summary):
    """
    Send a summary of an email to the owner of the email.
    Args:
        service: The Gmail API service object.
        owner: The owner of the email.
        email: The email object.
        summary: The summary of the email.
    Returns:
        The message ID of the sent message.
    """
    subject = _normalize_subject(email.subject)
    message = _make_message(
        owner,
        owner,  # Always the authenticated account, never a model-selected address.
        "AI Summary: " + subject,
        f"From: {email.sender}\nSubject: {subject}\n\n{summary}",
        **{"X-Seminar-Assistant": "summary"},
    )
    return service.users().messages().send(
        userId="me", body={"raw": encode_message(message)},
    ).execute()
