from typing import Optional

from pydantic import BaseModel


class Email(BaseModel):
    id: str  # The id of the email.
    labels: list[str]  # The labels of the email.
    sender_email: str  # The sender of the email.
    receiver_email: str  # The receiver of the email.
    time: str  # The time the email was sent.
    subject: str  # The subject of the email.
    snippet: str  # The snippet of the email.
    text: str  # The text of the email.
    size: int  # The size of the email.


class EmailDetails(BaseModel):
    """Represents a single email."""

    keywords: list[str]  # The keywords that the email contains.
    sender: Optional[str]  # The name of the sender.
    topic: Optional[str]  # The main topic of the email.
