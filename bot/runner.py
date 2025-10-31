import asyncio
import os
import re
from concurrent.futures import Future
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
_client_run_future: Optional[Future] = None


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


def _extract_bad_msg_code(exc: BadMsgNotification) -> Optional[int]:
    for attr in ("value", "code"):
        value = getattr(exc, attr, None)
        if value is not None:
            try:
                return int(value)
            except (TypeError, ValueError):
                continue
    match = re.search(r"\[(\d+)\]", str(exc))
    if match:
        return int(match.group(1))
    return None


def _delete_session_artifacts(session_name: str) -> None:
    candidates = {
        os.path.join(DOWNLOAD_DIRECTORY, f"{session_name}.session"),
        os.path.join(DEFAULT_DOWNLOAD_DIRECTORY, f"{session_name}.session"),
    }
    extra = set()
    for base in list(candidates):
        extra.add(f"{base}-journal")
        extra.add(f"{base}.journal")
    candidates.update(extra)

    for path in candidates:
        try:
            if os.path.exists(path):
                os.remove(path)
                LOGGER.warning("Removed stale session file at %s", path)
        except OSError as exc:
            LOGGER.error("Failed to remove session file %s: %s", path, exc)


def _run_client_blocking() -> None:
    session_name = "G-DriveBot"
    attempts = 0

    while attempts < 2:
        client = get_client(session_name=session_name)
        try:
            client.run()
            return
        except BadMsgNotification as exc:
            attempts += 1
            code = _extract_bad_msg_code(exc)
            if code == 16 and attempts < 2:
                LOGGER.warning(
                    "Telegram reported a time desynchronization (BadMsgNotification). "
                    "Clearing local session data and retrying."
                )
                _delete_session_artifacts(session_name)
                _set_client(None)
                continue
            raise


def _stop_client_blocking() -> None:
    client = get_client()
    if getattr(client, "is_connected", False):
        client.stop()


async def start_bot() -> Client:
    """
    Async helper for runtimes (e.g. FastAPI) that already manage an event loop.
    Ensures we only call `Client.start()` once.
    """
    global _client_run_future
    client = get_client(session_name="G-DriveBot")
    if _client_run_future and not _client_run_future.done():
        return client

    loop = asyncio.get_running_loop()
    LOGGER.info("Starting bot in background thread.")
    _client_run_future = loop.run_in_executor(None, _run_client_blocking)
    await asyncio.sleep(0.1)
    return client


async def stop_bot() -> None:
    client = get_client()
    global _client_run_future
    if _client_run_future and not _client_run_future.done():
        LOGGER.info("Stopping bot from async context.")
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _stop_client_blocking)
        try:
            await asyncio.wait_for(asyncio.wrap_future(_client_run_future), timeout=10)
        except Exception:
            LOGGER.warning("Timed out waiting for bot thread to terminate.")
        _client_run_future = None
