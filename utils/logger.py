import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_error_logging() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("video_echo_bot")
    logger.setLevel(logging.ERROR)

    if logger.handlers:
        return logger

    handler = TimedRotatingFileHandler(
        filename="logs/errors.log",
        when="midnight",
        interval=1,
        backupCount=30,
        utc=True,
        encoding="utf-8",
    )
    handler.setLevel(logging.ERROR)
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )

    logger.addHandler(handler)
    logger.propagate = False
    return logger


def setup_activity_logging() -> logging.Logger:
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger("video_echo_bot_activity")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    handler = TimedRotatingFileHandler(
        filename="logs/activity.log",
        when="midnight",
        interval=1,
        backupCount=30,
        utc=True,
        encoding="utf-8",
    )
    handler.setLevel(logging.INFO)
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )

    logger.addHandler(handler)
    logger.propagate = False
    return logger