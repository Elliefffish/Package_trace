import logging
import logging.handlers
import os
import pathlib

from dotenv import load_dotenv

from .configs.db_config import DATABASE_DIR
from .configs.log_config import (
    LOG_BACKUP_COUNT,
    LOG_FILE_DIR,
    LOG_FILE_MAX_SIZE,
    LOG_FILE_NAME,
)
from .configs.platform_config import PLATFORM
from .models import Database, ParcelTable, PlatformTable, SubscriptionTable

ROOT_DIR = pathlib.Path(__file__).parent.parent


def init_db():
    """Initialize database"""

    # Create data directory if not exists
    (ROOT_DIR / DATABASE_DIR).mkdir(parents=True, exist_ok=True)

    # Create tables
    with Database() as db:
        platform_table = PlatformTable(db)
        platform_table.create_table()
        # Insert platform data
        for platform in PLATFORM:
            platform_table.insert(platform)
        ParcelTable(db).create_table()
        SubscriptionTable(db).create_table()


def get_log_handler() -> logging.Handler:
    """
    Get logging handler

    Returns
    -------
    logging.Handler
        logging handler
    """

    # Create logs directory if not exists
    pathlib.Path(ROOT_DIR / LOG_FILE_DIR).mkdir(parents=True, exist_ok=True)

    # Create RotatingFileHandler
    handler = logging.handlers.RotatingFileHandler(
        filename=ROOT_DIR / LOG_FILE_DIR / LOG_FILE_NAME,
        encoding="utf-8",
        maxBytes=LOG_FILE_MAX_SIZE,
        backupCount=LOG_BACKUP_COUNT,
    )
    return handler


def get_discord_bot_token() -> str:
    """
    Get discord bot token from environment variable

    Returns
    -------
    str
        discord bot token
    """

    load_dotenv()
    discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")
    if not discord_bot_token:
        logging.error("DISCORD_BOT_TOKEN is not set")
        exit(1)
    return discord_bot_token
