import base64
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore
from icecream import ic

from config import Config
from models.email import Email
from src.utils.text_cleaner import clean_text, parse_html


class GmailFetcher:

    def __init__(self, config: Config) -> None:
        self._config = config
        self._token_path = self._config.token_path
        self._credentials_path = self._config.credentials_path
        self._scopes = self._config.gmail_scopes
        self._load_credentials()

    def _load_credentials(self) -> None:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self._token_path):
            creds = Credentials.from_authorized_user_file(
                self._token_path, self._scopes
            )
        # If there are no (valid) credentials available, log in is needed
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self._credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found at '{self._credentials_path}'."
                        f"Please provide a valid path to the credentials file"
                        f"or create a new Google Cloud project and download the credentials file."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self._credentials_path, self._scopes
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self._token_path, "w") as token:
                token.write(creds.to_json())
        self._creds = creds

    def get_labels(self) -> list[str]:
        try:
            service = build("gmail", "v1", credentials=self._creds)
            res_list = (
                service.users()
                .labels()
                .list(
                    userId="me", labelIds=["INBOX"], q="from:specific email, is:unread"
                )
                .execute()
            )
            results = res_list.get("labels", [])
            return [res["name"] for res in results]
        except HttpError as error:
            # TODO Handle errors from gmail API.
            print(f"An error occurred: {error}")
            return []

    def _fetch_messages(self, limit: int) -> list[dict]:
        try:
            service = build("gmail", "v1", credentials=self._creds)
            res_list = service.users().messages().list(userId="me").execute()
            results = res_list.get("messages", [])

            if not results:
                print("No results found.")
                return []
            messages = []
            for res in results[:limit]:
                message = (
                    service.users()
                    .messages()
                    .get(userId="me", id=res["id"], format="full")
                    .execute()
                )
                messages.append(message)
            return messages
        except HttpError as error:
            # TODO Handle errors from gmail API.
            print(f"An error occurred: {error}")
            return []

    def _parse_message(self, message: dict) -> Email:
        message_id = message.get("id", "")
        labels = message.get("labelIds", [])
        headers = message.get("payload", {}).get("headers", [])
        sender_email = ""
        receiver_email = ""
        time = ""
        subject = ""
        for header in headers:
            if header["name"] == "From":
                sender_email = header["value"].split("<")[1].split(">")[0]
            if header["name"] == "Delivered-To":
                receiver_email = header["value"]
            if header["name"] == "Date":
                time = header["value"]
            if header["name"] == "Subject":
                subject = header["value"]
        snippet = message.get("snippet", "")
        payload = message.get("payload", {}).get("body", {}).get("data", "")
        text = base64.urlsafe_b64decode(payload.encode("ASCII")).decode("utf-8")
        size = message.get("sizeEstimate", -1)
        email = Email(
            id=message_id,
            labels=labels,
            sender_email=sender_email,
            receiver_email=receiver_email,
            time=time,
            subject=subject,
            snippet=clean_text(snippet),
            text=parse_html(text),
            size=size,
        )
        return email

    def get_emails(self, limit: int = 10) -> list[Email]:
        raw_messages = self._fetch_messages(limit=limit)
        return [self._parse_message(message) for message in raw_messages]

    def get_snippets(self, limit: int = 10) -> dict[str, str]:
        emails = self.get_emails(limit=limit)
        return {email.id: email.text for email in emails}


if __name__ == "__main__":
    config = Config()
    fetcher = GmailFetcher(config=config)
    # ic(fetcher.get_labels())
    # ic(fetcher.get_snippets(limit=10))
    ic(fetcher.get_emails(limit=3))
