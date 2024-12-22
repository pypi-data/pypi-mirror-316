"""Automatic database migrations manager."""

import os
import logging
from pathlib import Path
from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine

from .utils import get_default_db_path

logger = logging.getLogger(__name__)

def check_and_run_migrations():
    """Check and run any pending database migrations."""
    try:
        db_path = get_default_db_path()
        engine = create_engine(f"sqlite:///{db_path}")

        # Create migrations table if it doesn't exist
        with engine.connect() as conn:
            context = MigrationContext.configure(conn)
            current_rev = context.get_current_revision()

        if current_rev is None:
            # Run migrations
            config = Config()
            migrations_dir = os.path.join(os.path.dirname(__file__), "migrations")
            config.set_main_option("script_location", migrations_dir)
            config.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
            
            command.upgrade(config, "head")
            logger.info("Database migrations completed successfully")
    except Exception as e:
        logger.error(f"Failed to run migrations: {e}")
        # Don't raise the exception - allow the application to continue
        # The user can manually initialize the DB later if needed