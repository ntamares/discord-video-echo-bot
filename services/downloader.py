import yt_dlp, os, uuid
from typing import Any, cast
from yt_dlp.utils import DownloadError as YtDlpDownloadError

DOWNLOAD_DIR = "tmp"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def _normalize_url(url: str) -> str:
    return url.strip().strip("<>")


def download_video(url: str) -> str:
    if not isinstance(url, str):
        raise ValueError("Invalid URL type")

    normalized_url = _normalize_url(url)
    if not normalized_url:
        raise ValueError("Invalid URL")

    file_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_DIR, f"{file_id}.mp4")

    ydl_opts: dict[str, str | bool] = {
        "outtmpl": output_path,
        "format": "mp4/best",
        "quiet": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(cast(Any, ydl_opts)) as ydl:
            ydl.download([normalized_url])
    except YtDlpDownloadError as exc:
        raise ValueError("Could not download media from this link") from exc

    return output_path