import importlib
import logging
import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

LOGGER = logging.getLogger(__name__)
DATABASE_URL = None
DEFAULT_DATA_DIR = None


def _create_session(url_string: str) -> scoped_session:
  engine_kwargs = {}
  url = make_url(url_string)
  if url.drivername == 'sqlite':
      db_path = url.database or ''
      db_dir = os.path.dirname(db_path)
      if db_path and db_dir and not os.path.isdir(db_dir):
          os.makedirs(db_dir, exist_ok=True)
      engine_kwargs["connect_args"] = {"check_same_thread": False}
  engine_kwargs["pool_pre_ping"] = True
  engine = create_engine(url_string, **engine_kwargs)
  BASE.metadata.bind = engine
  BASE.metadata.create_all(engine)
  return scoped_session(sessionmaker(bind=engine, autoflush=False))


def _sqlite_fallback_url(original_url: str) -> Optional[str]:
  try:
    url = make_url(original_url)
  except Exception:
    return None
  if url.drivername != 'sqlite':
    return None
  fallback_path = os.path.join(DEFAULT_DATA_DIR, "gdrive.db")
  fallback_url = f"sqlite:///{fallback_path}"
  if fallback_url == original_url:
    return None
  return fallback_url


def start() -> scoped_session:
  global DATABASE_URL, DEFAULT_DATA_DIR, LOGGER

  bot_module = importlib.import_module("bot")
  if DEFAULT_DATA_DIR is None:
    DEFAULT_DATA_DIR = getattr(bot_module, "DEFAULT_DATA_DIR", os.getcwd())
  if LOGGER is logging.getLogger(__name__):
    LOGGER = getattr(bot_module, "LOGGER", LOGGER)
  if DATABASE_URL is None:
    DATABASE_URL = getattr(bot_module, "DATABASE_URL")

  candidate_urls = [DATABASE_URL]
  fallback_url = _sqlite_fallback_url(DATABASE_URL)
  if fallback_url:
    candidate_urls.append(fallback_url)

  last_exc: Optional[Exception] = None
  for idx, candidate in enumerate(candidate_urls):
    is_last_attempt = idx == len(candidate_urls) - 1
    try:
      session = _create_session(candidate)
      current_bot_url = getattr(bot_module, "DATABASE_URL", candidate)
      if candidate != current_bot_url:
        LOGGER.warning(
            'DATABASE_URL "%s" is not writable. Falling back to "%s".',
            current_bot_url,
            candidate,
        )
        setattr(bot_module, "DATABASE_URL", candidate)
        DATABASE_URL = candidate
      return session
    except OSError as exc:
      last_exc = exc
      if is_last_attempt:
        LOGGER.error('Unable to prepare database path for "%s": %s', candidate, exc)
      else:
        LOGGER.warning('Unable to prepare database path for "%s": %s', candidate, exc)
    except Exception as exc:
      last_exc = exc
      if is_last_attempt:
        LOGGER.error('Failed to initialize database engine with url %s: %s', candidate, exc)
      else:
        LOGGER.warning('Failed to initialize database engine with url %s: %s', candidate, exc)

  LOGGER.error(
      'Exiting because the database engine could not be initialized after trying %s.',
      candidate_urls,
  )
  if last_exc:
    raise SystemExit(1) from last_exc
  raise SystemExit(1)


BASE = declarative_base()
SESSION = start()
