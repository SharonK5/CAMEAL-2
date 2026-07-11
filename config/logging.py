"""
config/logging.py

Central logging configuration for the CAMEAL Framework.

Context-Aware Adaptation, Monitoring,
Evaluation, Accountability and Learning (CAMEAL)

Author: Sharon Rhodah Kaitano
"""

from __future__ import annotations

import logging
import logging.handlers
from pathlib import Path

# ==========================================================
# LOG DIRECTORY
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "cameal.log"

# ==========================================================
# LOG FORMAT
# ==========================================================

LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | "
    "%(name)s | %(filename)s:%(lineno)d | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ==========================================================
# LOGGER CONFIGURATION
# ==========================================================

def configure_logging(level: int = logging.INFO) -> None:
    """
    Configure application-wide logging.

    Call once during application startup.
    """

    logger = logging.getLogger()

    if logger.handlers:
        return

    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT
    )

    # Console
    console = logging.StreamHandler()
    console.setFormatter(formatter)

    # Rotating file
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,   # 10 MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file_handler)


# ==========================================================
# LOGGER FACTORY
# ==========================================================

def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger.

    Example:
        logger = get_logger(__name__)
    """
    return logging.getLogger(name)
