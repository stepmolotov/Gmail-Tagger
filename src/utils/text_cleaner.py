import re
from html import unescape

import trafilatura


def clean_text(text: str) -> str:
    # decode HTML entities
    cleaned_text = unescape(text)
    # remove unicode characters
    cleaned_text = re.sub(r"[^\x00-\x7F]+", "", cleaned_text)
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    return cleaned_text


def parse_html(html: str) -> str:
    parsed_html = trafilatura.html2txt(html)
    return clean_text(parsed_html)
