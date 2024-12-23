import logging
import logging.config
from logging import getLogger

__all__ = [
    "download_data",
    "kcat",
    "km",
]

from . import kcat, km
from ._download import download_data

logger = getLogger("deepmolecules")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(
        "{asctime} {levelname:8s} {message}",
        style="{",
    ),
)
logger.addHandler(handler)
