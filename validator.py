import re

URL_REGEX = r"https?://[^\s]+"

def is_valid_url(text: str) -> bool:
    return re.match(URL_REGEX, text) is not None
