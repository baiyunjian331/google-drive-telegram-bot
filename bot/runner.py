import asyncio
import os
from typing import Optional

from pyrogram import Client
from pyrogram.errors import BadMsgNotification

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


def _delete_session_artifacts(session_name: str) -> None:
    base_paths = {
        os.path.join(DOWNLOAD_DIRECTORY, f"{session_name}.session"),
        os.path.join(DEFAULT_DOWNLOAD_DIRECTORY, f"{session_name}.session"),
    }
    # Include journal variants used by sqlite-based storage
    extra_paths = set()
    for base_path in base_paths:
        extra_paths.add(f"{base_path}-journal")
        extra_paths.add(f"{base_path}.journal")
    candidates = base_paths.union(extra_paths)

    for path in candidates:
        try:
            if os.path.exists(path):
                os.remove(path)
                LOGGER.warning("Removed stale session file at %s", path)
        except OSError as exc:
            LOGGER.error("Failed to remove session file %s: %s", path, exc)


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


def _set_client(client: Optional[Client]) -> None:
    global _client
    _client = client


def get_client(session_name: str = "G-DriveBot") -> Client:
    if _client is None:
        _set_client(create_client(session_name=session_name))
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
    session_name = "G-DriveBot"
    attempts = 0

    while attempts < 2:
        client = get_client(session_name=session_name)
        if getattr(client, "is_connected", False):
            return client

        LOGGER.info("Starting bot in async context.")
        try:
            await client.start()
            return client
        except BadMsgNotification as exc:
            attempts += 1
            if exc.value == 16 and attempts < 2:
                LOGGER.warning(
                    "Telegram reported a time desynchronization (BadMsgNotification). "
                    "Clearing local session data and retrying."
                )
                await asyncio.sleep(1)
                _delete_session_artifacts(session_name)
                _set_client(None)
                continue
            raise

    raise RuntimeError("Failed to start Pyrogram client after retrying session reset.")


async def stop_bot() -> None:
    client = get_client()
    if getattr(client, "is_connected", False):
        LOGGER.info("Stopping bot from async context.")
        await client.stop()
