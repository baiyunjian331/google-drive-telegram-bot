import os
from typing import Optional

from pyrogram import Client

import bot
from bot import (
    APP_ID,
    API_HASH,
    BOT_TOKEN,
    DOWNLOAD_DIRECTORY,
    LOGGER,
    DEFAULT_DOWNLOAD_DIRECTORY,
)


_client: Optional[Client] = None


def _ensure_download_directory() -> str:
    target_dir = DOWNLOAD_DIRECTORY
    try:
        if not os.path.isdir(target_dir):
            LOGGER.info("Creating download directory at %s", target_dir)
            os.makedirs(target_dir, exist_ok=True)
        return target_dir
    except OSError as exc:
        fallback = DEFAULT_DOWNLOAD_DIRECTORY
        if os.path.abspath(fallback) != os.path.abspath(target_dir):
            LOGGER.warning(
                "Failed to access download directory %s: %s. Falling back to %s",
                target_dir,
                exc,
                fallback,
            )
            try:
                os.makedirs(fallback, exist_ok=True)
            except OSError as fallback_exc:
                LOGGER.error(
                    "Unable to prepare fallback download directory %s: %s",
                    fallback,
                    fallback_exc,
                )
                raise
            bot.DOWNLOAD_DIRECTORY = fallback
            globals()["DOWNLOAD_DIRECTORY"] = fallback
            LOGGER.info("Using fallback download directory at %s", fallback)
            return fallback
        raise


def create_client(session_name: str = "G-DriveBot") -> Client:
    """
    Lazily instantiate the Pyrogram client so both CLI and web runtimes
    can share the same initialization logic.
    """
    plugins = dict(root="bot/plugins")
    workdir = _ensure_download_directory()
    LOGGER.debug("Initializing Pyrogram client with workdir=%s", workdir)
    return Client(
        session_name,
        bot_token=BOT_TOKEN,
        api_id=APP_ID,
        api_hash=API_HASH,
        plugins=plugins,
        parse_mode="markdown",
        workdir=workdir,
    )


def get_client(session_name: str = "G-DriveBot") -> Client:
    global _client
    if _client is None:
        _client = create_client(session_name=session_name)
    return _client


def run_bot() -> None:
    """
    Synchronous entry point used by `python -m bot`.
    """
    client = get_client()
    LOGGER.info("Starting bot!")
    client.run()
    LOGGER.info("Bot stopped!")


async def start_bot() -> Client:
    """
    Async helper for runtimes (e.g. FastAPI) that already manage an event loop.
    Ensures we only call `Client.start()` once.
    """
    client = get_client(session_name="G-DriveBot")
    if not getattr(client, "is_connected", False):
        LOGGER.info("Starting bot in async context.")
        await client.start()
    return client


async def stop_bot() -> None:
    client = get_client()
    if getattr(client, "is_connected", False):
        LOGGER.info("Stopping bot from async context.")
        await client.stop()
