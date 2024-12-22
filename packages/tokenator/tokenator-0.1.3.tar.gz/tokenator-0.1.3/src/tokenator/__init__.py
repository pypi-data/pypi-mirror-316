"""Tokenator - Track and analyze your OpenAI API token usage and costs."""

import logging
from .client_openai import OpenAIWrapper
from . import usage
from .utils import get_default_db_path, is_colab

__version__ = "0.1.0"
__all__ = ["OpenAIWrapper", "usage", "get_default_db_path"]

logger = logging.getLogger(__name__)

try:
    if not is_colab():
        from .migrations import check_and_run_migrations
        check_and_run_migrations()
    else:
        logger.info("Running in Colab environment - skipping migrations")
except Exception as e:
    logger.warning(f"Failed to run migrations, but continuing anyway: {e}") 