import os
import sys
import logging
from typing import Tuple


def _prepare_data_directory() -> Tuple[str, bool]:
  """
  Ensure a writable base directory exists for data that should persist
  across restarts (e.g. SQLite DB, downloads). Preference order:
  1. DATA_DIR environment variable.
  2. /data on POSIX systems (Hugging Face Spaces uses this path).
  3. A `data` folder inside the current working directory.
  """
  candidates = []
  env_data_dir = os.environ.get("DATA_DIR")
  if env_data_dir:
    candidates.append(env_data_dir)
  if os.name == "posix":
    candidates.append("/data")
  candidates.append(os.path.join(os.getcwd(), "data"))

  for candidate in candidates:
    candidate = os.path.abspath(candidate)
    try:
      os.makedirs(candidate, exist_ok=True)
      return candidate, False
    except OSError:
      continue

  return os.getcwd(), True


DEFAULT_DATA_DIR, _data_dir_fallback_used = _prepare_data_directory()
DEFAULT_DOWNLOAD_DIRECTORY = os.path.join(DEFAULT_DATA_DIR, "downloads")
LOG_FILE_PATH = os.path.join(DEFAULT_DATA_DIR, "log.txt")

handlers = [logging.StreamHandler()]
try:
  handlers.insert(0, logging.FileHandler(LOG_FILE_PATH))
except OSError as exc:
  print(f"[bot] Unable to create log file at {LOG_FILE_PATH}: {exc}", file=sys.stderr)

logging.basicConfig(
    level=logging.INFO,
    handlers=handlers,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

if _data_dir_fallback_used:
  LOGGER.warning(
      'All candidate data directories were unavailable. Falling back to %s',
      DEFAULT_DATA_DIR,
  )

ENV = bool(os.environ.get('ENV', False))
try:
  if ENV:
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    APP_ID = os.environ.get('APP_ID')
    API_HASH = os.environ.get('API_HASH')
    DATABASE_URL = os.environ.get('DATABASE_URL')
    SUDO_USERS = os.environ.get('SUDO_USERS', '')
    SUPPORT_CHAT_LINK = os.environ.get('SUPPORT_CHAT_LINK')
    download_directory_raw = os.environ.get("DOWNLOAD_DIRECTORY", "")
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
    download_directory_raw = config.DOWNLOAD_DIRECTORY
    G_DRIVE_CLIENT_ID = config.G_DRIVE_CLIENT_ID
    G_DRIVE_CLIENT_SECRET = config.G_DRIVE_CLIENT_SECRET

  if not download_directory_raw or download_directory_raw.strip() in {"./downloads/", "./downloads"}:
    download_directory_raw = DEFAULT_DOWNLOAD_DIRECTORY
  DOWNLOAD_DIRECTORY = os.path.abspath(download_directory_raw)

  if not DATABASE_URL:
    default_sqlite_path = os.path.join(DEFAULT_DATA_DIR, "gdrive.db")
    DATABASE_URL = f"sqlite:///{default_sqlite_path}"
    LOGGER.warning(
        'DATABASE_URL not provided. Falling back to local SQLite database at %s',
        default_sqlite_path
    )

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
