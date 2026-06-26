import re

URL_PATTERN = re.compile(r"https?://\S+")
SUPPORTED_PATTERNS = (
    re.compile(r"instagram\.com/reel/"),
    re.compile(r"facebook\.com/reel/"),
    re.compile(r"youtube\.com/watch\?v="),
    re.compile(r"youtube\.com/shorts/"),
    re.compile(r"v\.redd\.it/"),
    re.compile(r"reddit\.com/r/"),
)

def _sanitize_url(url: str) -> str:
    cleaned = url.strip().strip("<>")
    return cleaned.rstrip(".,!?:;)]}'\"")

def extract_supported_url(message_content: str) -> str | None:
    for matched_url in URL_PATTERN.findall(message_content):
        url = _sanitize_url(matched_url)
        if not url:
            continue

        if any(pattern.search(url) for pattern in SUPPORTED_PATTERNS):
            return url
        
    return None