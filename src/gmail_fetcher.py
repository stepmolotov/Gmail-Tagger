import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from icecream import ic


class GmailFetcher:

    def __init__(self) -> None:
        self._token_path = "../resources/token.json"
        self._credentials_path = "../resources/credentials.json"
        self._scopes = ["https://www.googleapis.com/auth/gmail.readonly"]
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
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
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
            res_list = service.users().labels().list(userId="me").execute()
            results = res_list.get("labels", [])
            return [res["name"] for res in results]
        except HttpError as error:
            # TODO Handle errors from gmail API.
            print(f"An error occurred: {error}")
            return []

    def get_messages(self, limit: int) -> list[dict]:
        try:
            service = build("gmail", "v1", credentials=self._creds)
            res_list = service.users().messages().list(userId="me").execute()
            results = res_list.get("messages", [])

            if not results:
                print("No results found.")
                return []
            print(f"Results: {len(results)}")
            messages = []
            for res in results[:limit]:
                message = (
                    service.users().messages().get(userId="me", id=res["id"]).execute()
                )
                messages.append(message)
            return messages
        except HttpError as error:
            # TODO Handle errors from gmail API.
            print(f"An error occurred: {error}")
            return []

    def get_snippets(self, limit: int = 10) -> dict[str, str]:
        messages = self.get_messages(limit=limit)
        return {
            message.get("id", ""): message.get("snippet", "") for message in messages
        }


if __name__ == "__main__":
    fetcher = GmailFetcher()
    ic(fetcher.get_labels())
    ic(fetcher.get_snippets(limit=10))
