import re

INSTAGRAM_PATTERN = re.compile(r"https?://(?:www\.)?instagram\.com/reel/")
FACEBOOK_PATTERN = re.compile(r"https?://(?:www\.)?facebook\.com/.*/reel/")
TIKTOK_PATTERN = re.compile(r"https?://(?:www\.)?tiktok\.com/")

def contains_supported_link(message_content: str) -> bool:
    return any([
        INSTAGRAM_PATTERN.search(message_content),
        FACEBOOK_PATTERN.search(message_content),
        TIKTOK_PATTERN.search(message_content),
    ])