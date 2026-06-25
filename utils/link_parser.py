import re

URL_PATTERN = re.compile(r"https?://\S+")
SUPPORTED_PATTERNS = (
    re.compile(r"instagram\.com/p/"),
    re.compile(r"instagram\.com/reel/"),
    re.compile(r"facebook\.com/reel/"),
)

def extract_supported_url(message_content: str) -> str | None:
    for url in URL_PATTERN.findall(message_content):
        if any(pattern.search(url) for pattern in SUPPORTED_PATTERNS):
            return url
        
    return None