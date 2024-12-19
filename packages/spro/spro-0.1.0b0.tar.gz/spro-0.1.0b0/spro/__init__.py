import logging
import os
from spro.spro import Spro, AsyncSpro
from spro._exceptions import (
    SProError,
    APIError,
    InvalidEntityError,
    InvalidAPIKeyError,
    AuthenticationError,
    ConfigurationError,
    ValidationError,
)

__version__ = "0.1.0"
__all__ = [
    "Spro",
    "AsyncSpro",
    "SProError",
    "APIError",
    "InvalidEntityError",
    "InvalidAPIKeyError",
    "AuthenticationError",
    "ConfigurationError",
    "ValidationError",
]
# Create a logger for the SECURE_PROMPTS module
logger: logging.Logger = logging.getLogger("spro")


def _basic_config() -> None:
    """Set up basic configuration for logging with a specific format and date format."""
    try:
        logging.basicConfig(
            format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
            filename="spro.log",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    except Exception as e:
        logger.error("Failed to configure logging: %s", e)


def setup_logging() -> None:
    """Set up logging based on the SECURE_PROMPTS_LOGGING_LEVEL environment variable."""
    _basic_config()

    # Fetch logging level from environment variable
    env = os.getenv("SPRO_LOGGING_LEVEL", "INFO").upper()

    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    # Set logging level based on the environment variable, defaulting to INFO
    if env in level_map:
        logger.setLevel(level_map[env])
    else:
        logger.setLevel(logging.INFO)
        logger.warning("Unknown logging level: %s, defaulting to INFO", env)


# Initialize logging configuration when the module is imported
setup_logging()
logger.debug("Logger setup complete for Spro")
