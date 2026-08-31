from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOGGER_NAME = "anki_ai_workspace"
LOG_FILENAME = "anki_ai_workspace.log"


def logger() -> logging.Logger:
    result = logging.getLogger(LOGGER_NAME)
    if not result.handlers:
        result.addHandler(logging.NullHandler())
    return result


def configure_log(anki_base_folder: str | Path) -> Path:
    """Write operational events only; card and chat content are never logged."""

    path = Path(anki_base_folder) / "logs" / LOG_FILENAME
    path.parent.mkdir(parents=True, exist_ok=True)
    result = logging.getLogger(LOGGER_NAME)
    result.setLevel(logging.INFO)
    result.propagate = False
    for handler in tuple(result.handlers):
        if isinstance(handler, RotatingFileHandler):
            return path
        result.removeHandler(handler)
    handler = RotatingFileHandler(
        path, maxBytes=500_000, backupCount=2, encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    result.addHandler(handler)
    result.info("logging configured path=%s", path)
    return path
