"""Run Gmail authorization directly; no model or mailbox processing is involved."""

from pathlib import Path

from lib.gmail_auth import connect_gmail


def main():
    service = connect_gmail(Path(__file__).resolve().parent)
    owner = service.users().getProfile(userId="me").execute()["emailAddress"]
    print(f"CONNECTED | {owner}")
    print("OAuth is ready. No messages were processed.")


if __name__ == "__main__":
    main()
