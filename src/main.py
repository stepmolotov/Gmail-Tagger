from icecream import ic

from src.gmail_fetcher import GmailFetcher
from src.mail_analyser import MailAnalyser

if __name__ == "__main__":

    fetcher = GmailFetcher()
    analyser = MailAnalyser()

    mails = fetcher.get_emails(limit=3)
    for mail in mails:
        ic(mail)
        mail_details = analyser.get_details(mail)
        ic(mail_details)
