import re

def parse_allowed_channels(raw_value: str) -> set[int]:
    return {int(channel_id) for channel_id in re.findall(r"\d+", raw_value)}