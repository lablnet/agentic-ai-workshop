"""Prepared Gmail reads, MIME handling, draft creation and self-summary delivery."""

import base64
from email import policy
from email.parser import BytesParser
from email.utils import parseaddr
from html.parser import HTMLParser

from .models import IncomingEmail


class TextFromHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)


def list_incoming_ids(service):
    """
    List the IDs of incoming emails.
    Args:
        service: The Gmail API service object.
    Returns:
        A list of email IDs.
    """
    # Limit the workshop to explicitly marked test emails, not the whole inbox.
    ids = []
    page = None
    while True:
        # List the emails in the inbox.
        result = service.users().messages().list(
            userId="me", q='in:inbox subject:"AI-DEMO" -from:me',
            maxResults=100, pageToken=page,
        ).execute()
        # Add the email IDs to the list.
        ids.extend(message["id"] for message in result.get("messages", []))
        # Get the next page token.
        page = result.get("nextPageToken")
        # If there is no next page token, return the list of email IDs.
        if not page:
            return ids


def read_email(service, gmail_id, owner):
    """
    Read an email by its ID.
    Args:
        service: The Gmail API service object.
        gmail_id: The ID of the email.
        owner: The owner of the email.
    Returns:
        The email object.
    """
    # Get the email by its ID.
    result = service.users().messages().get(userId="me", id=gmail_id, format="raw").execute()
    # Decode the raw email.
    raw = base64.urlsafe_b64decode(result["raw"] + "=" * (-len(result["raw"]) % 4))
    # Parse the email.
    message = BytesParser(policy=policy.default).parsebytes(raw)
    # Get the sender.
    sender = parseaddr(str(message.get("From", "")))[1]
    # Also exclude assistant summaries if a user's filter/query changes later.
    if "SENT" in result.get("labelIds", []) or sender.lower() == owner.lower():
        return None
    if message.get("X-Seminar-Assistant"):
        return None

    # Get the body of the email.
    body_part = message.get_body(preferencelist=("plain", "html"))
    body = body_part.get_content() if body_part else ""
    if body_part and body_part.get_content_type() == "text/html":
        parser = TextFromHTML()
        parser.feed(body)
        body = "\n".join(parser.text)
    if not body.strip():
        raise ValueError("No readable email body. This demo does not process attachments.")
    if len(body) > 20000:
        raise ValueError("Email exceeds the demo limit of 20,000 body characters.")
    # Return the email object.
    return IncomingEmail(
        gmail_id=gmail_id, thread_id=result["threadId"], sender=sender,
        reply_to=parseaddr(str(message.get("Reply-To", "")))[1] or sender,
        subject=str(message.get("Subject", "(no subject)")), body=body,
        message_id=str(message.get("Message-ID", "")),
        references=str(message.get("References", "")),
    )


def encode_message(message):
    """
    Encode a message.
    Args:
        message: The message to encode.
    Returns:
        The encoded message.
    """
    # Encode the message.
    return base64.urlsafe_b64encode(message.as_bytes()).decode("ascii")
