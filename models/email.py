from typing import Optional

from pydantic import BaseModel


class Email(BaseModel):
    id: Optional[str]  # The id of the email.
    labels: list[str]  # The labels of the email.
    sender_email: Optional[str]  # The sender of the email.
    receiver_email: Optional[str]  # The receiver of the email.
    time: Optional[str]  # The time the email was sent.
    subject: Optional[str]  # The subject of the email.
    snippet: Optional[str]  # The snippet of the email.
    text: Optional[str]  # The text of the email.
    size: Optional[int]  # The size of the email.


class EmailDetails(BaseModel):
    """Represents a single email."""

    keywords: list[str]  # The keywords that the email contains.
    sender: Optional[str]  # The name of the sender.
    topic: Optional[str]  # The main topic of the email.
