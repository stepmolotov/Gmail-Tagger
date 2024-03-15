import os
import marvin
import json

from icecream import ic

from models.email import Email, EmailDetails


class MailAnalyser:
    OA_KEY = "OA_KEY"

    def __init__(self) -> None:
        marvin.settings.openai.api_key = self.OA_KEY
        marvin.settings.openai.chat.completions.model = "gpt-3.5-turbo"
        marvin.settings.llm_model = "gpt-3.5-turbo"
        marvin.settings.llm_temperature = 0
        marvin.settings.log_level = "INFO"

    def get_details(self, email: Email) -> EmailDetails:
        raw_input = (
            f"Subject: {email.subject}\nSnippet:{email.snippet}\nText:{email.text}"
        )
        email_details = marvin.extract(
            raw_input,
            EmailDetails,
            instructions="Get the top 5 keywords from the email text and identify sender and topic.",
        )
        if email_details:
            return email_details[0]
        return EmailDetails(keywords=[], sender=None, topic=None)


if __name__ == "__main__":
    email = Email(
        id="XXXXXX",
        labels=["CATEGORY_PROMOTIONS", "UNREAD", "INBOX"],
        sender_email="newsletter@gamesplanet.com",
        receiver_email="some_mail@gmail.com",
        time="Fri, 15 Mar 2024 11:13:14 +0000",
        subject="New but retro: Contra Operation Galuga (-20%), 🪖 Outcast 2 & SW Battlefront / Deals on Capcom, SEGA and more",
        snippet="Gamesplanet.com Facebook Twitter YouTube Pneumatic tube 15.03.2024 The classic platforming series returns with Contra: Operation Galuga Contra: Operation Galuga Contra: Operation Galuga Action / Arcade",
        text="Pneumatic tube 15.03.2024 The classic platforming series returns with Contra: Operation Galuga Contra: Operation Galuga Action / Arcade & Indie The legendary Contra series returns! This reimagining of the classic run-'n'-gun action game from the 80s features new stages, new enemies, new play mechanics, and co-op combat for up to 4 players! 34.99 -20% 27.99 Go on a new journey and face Ewoks again 49.99 -10% 26.40 Great Weekend Deals on Starfield, RE4 and much more -39% 36.85 -32% 22.50 -74% 10.39 -76% 8.31 -69% 7.99 -76% 8.31 -76% 8.31 -76% 8.31 -81% 9.58 -77% 11.66 -80% 3.19 All Bethesda Spring Deals -81% 6.39 -70% 9.89 -70% 9.59 -70% 14.99 -45% 18.14 -54% 22.99 -74% 6.46 -74% 6.20 Visit the Capcom Promo -82% 7.19 -53% 30.87 -57% 21.66 -78% 7.87 -71% 7.29 -86% 7.08 -86% 10.42 -87% 5.28 Check out Bandai Deals -24% 15.19 -24% 15.19 -22% 23.25 -61% 21.21 -63% 13.12 -62% 18.75 -71% 15.71 -72% 21.25 Show me the SEGA Promo -40% 29.99 -53% 23.32 -38% 31.00 -20% 34.39 -44% 22.39 -76% 9.59 -76% 9.59 -76% 21.15 -30% 24.49 -33% 8.52 -78% 7.87 -52% 19.99 -84% 7.99 -40% 25.79 -54% 18.39 -35% 16.24 -38% 31.00 -39% 18.99 -79% 7.44 See all Weekend Deals Hot Gaming News delivered right to your inbox [Video] Shin Megami Tensei V: Vengeance - Developer Spotlight Wong Sifu | 14.03.2024 [Video] Outcast - A New Beginning : Gameplay Deep Dive Wong Sifu | 12.03.2024 [Video] Contra: Operation Galuga - Launch, Gameplay & Character Trailers Wong Sifu | 12.03.2024 [FAQ] Horizon Forbidden West - Complete Edition System Requirements Revealed CraigB | 12.03.2024 [News] Dragon's Dogma 2: Create characters now - here's how! RafalM | 08.03.2024 Gamesplanet Submission Face Huge foes and more upcoming releases -10% 48.58 -10% 44.99 -10% 8.99 24.99 -5% 33.24 -15% 42.49 See all titles Coming Soon Visit our facebook page Gaming news, contests and vouchers are waiting for you! Congrats for reading through to the end of the newsletter!You found the princess. Gamesplanet Website Terms Legal Unsubscribe from Newsletter",
        size=91368,
    )
    analyser = MailAnalyser()
    ic(analyser.get_details(email))
    # EmailDetails(keywords=['Contra', 'Operation', 'Galuga', 'new', 'retro'], sender='Gamesplanet.com', topic='Gaming Deals')
