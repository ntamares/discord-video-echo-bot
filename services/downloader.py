import yt_dlp
import os
import uuid
from typing import Any, cast

DOWNLOAD_DIR = "tmp"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_video(url: str) -> str:
    file_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_DIR, f"{file_id}.mp4")

    ydl_opts: dict[str, str | bool] = {
        "outtmpl": output_path,
        "format": "mp4/best",
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(cast(Any, ydl_opts)) as ydl:
        ydl.download([url])

    return output_path