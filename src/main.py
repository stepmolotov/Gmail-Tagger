from icecream import ic

from config import Config
from src.gmail_fetcher import GmailFetcher
from src.mail_analyser import MailAnalyser

if __name__ == "__main__":
    config = Config()
    fetcher = GmailFetcher(config=config)
    analyser = MailAnalyser(config=config)

    mails = fetcher.get_emails(limit=10)
    for mail in mails:
        # ic(mail)
        mail_details = analyser.get_details(mail)
        ic(mail_details)
