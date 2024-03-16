from dotenv import load_dotenv
import os


class Config:

    def __init__(self) -> None:
        self._load_dot_env()

        # OpenAI API key
        self.oa_key = self._requried_var("OA_KEY")

        # Gmail API credentials
        self.gmail_scopes = ["https://www.googleapis.com/auth/gmail.readonly"]
        self.credentials_path = self._requried_var("CREDENTIALS_PATH")
        self.token_path = self._requried_var("TOKEN_PATH")

    def _load_dot_env(self) -> None:
        environment = os.environ.get("DOT_ENV_DEFAULTS") or "local"
        filename = f".env.{environment}"

        if not os.path.exists(filename):
            raise FileNotFoundError(f"Environment '{filename}' not found. Are you sure you're in the root directory?")

        self.env_filename = filename
        load_dotenv(filename)

    def _requried_var(self, var: str) -> str:
        var_value = os.getenv(var)
        if not var_value:
            raise ValueError(f"Environment variable '{var}' is required.")
        return var_value
