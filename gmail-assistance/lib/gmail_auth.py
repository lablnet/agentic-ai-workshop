"""Standalone Gmail OAuth setup and reusable connection function."""

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Read messages; create drafts and send the account owner's summaries.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",
          "https://www.googleapis.com/auth/gmail.compose"]


def connect_gmail(folder):
    token_path = folder / "token.json"
    credentials_path = folder / "credentials.json"
    credentials = None
    if token_path.exists():
        credentials = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        if not credentials.has_scopes(SCOPES):
            credentials = None
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            if not credentials_path.exists():
                raise FileNotFoundError("Download Desktop OAuth credentials to gmail-assistance/credentials.json.")
            flow = InstalledAppFlow.from_client_secrets_file(str(credentials_path), SCOPES)
            credentials = flow.run_local_server(port=0)
        token_path.write_text(credentials.to_json(), encoding="utf-8")
        token_path.chmod(0o600)
    return build("gmail", "v1", credentials=credentials, cache_discovery=False)

