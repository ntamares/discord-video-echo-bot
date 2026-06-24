import re

URL_PATTERN = re.compile(r"https?://\S+")

INSTAGRAM_PATTERN = re.compile(r"instagram\.com/reel/")
FACEBOOK_PATTERN = re.compile(r"facebook\.com/.*/reel/")
TIKTOK_PATTERN = re.compile(r"tiktok\.com/")


def extract_supported_url(message_content: str) -> str | None:
    urls = URL_PATTERN.findall(message_content)

    for url in urls:
        if (
            INSTAGRAM_PATTERN.search(url)
            or FACEBOOK_PATTERN.search(url)
            or TIKTOK_PATTERN.search(url)
        ):
            return url

    return None