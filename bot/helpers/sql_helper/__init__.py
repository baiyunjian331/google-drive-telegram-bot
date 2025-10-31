import importlib
import logging
import os
from typing import Iterable, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


LOGGER = logging.getLogger(__name__)


def _create_session(url_string: str) -> scoped_session:
  engine_kwargs = {"pool_pre_ping": True}
  url = make_url(url_string)
  if url.drivername == 'sqlite':
      db_path = url.database or ''
      if db_path:
          db_dir = os.path.dirname(db_path)
          if db_dir and not os.path.isdir(db_dir):
              os.makedirs(db_dir, exist_ok=True)
      engine_kwargs["connect_args"] = {"check_same_thread": False}
  engine = create_engine(url_string, **engine_kwargs)
  BASE.metadata.bind = engine
  BASE.metadata.create_all(engine)
  return scoped_session(sessionmaker(bind=engine, autoflush=False))


def _candidate_database_urls(base_url: str, default_data_dir: str) -> Iterable[str]:
  yield base_url
  try:
    parsed = make_url(base_url)
  except Exception:
    return
  if parsed.drivername != 'sqlite':
    return
  fallback_path = os.path.join(default_data_dir, "gdrive.db")
  fallback_url = f"sqlite:///{fallback_path}"
  if fallback_url != base_url:
    yield fallback_url


def start() -> scoped_session:
  global LOGGER

  bot_module = importlib.import_module("bot")
  default_data_dir = getattr(bot_module, "DEFAULT_DATA_DIR", os.getcwd())
  base_url = getattr(bot_module, "DATABASE_URL")
  LOGGER = getattr(bot_module, "LOGGER", LOGGER)

  candidates = list(_candidate_database_urls(base_url, default_data_dir))
  last_exc: Optional[Exception] = None

  for idx, candidate in enumerate(candidates):
    is_last_attempt = idx == len(candidates) - 1
    try:
      session = _create_session(candidate)
      if candidate != base_url:
        LOGGER.warning(
            'DATABASE_URL "%s" is not writable. Falling back to "%s".',
            base_url,
            candidate,
        )
        setattr(bot_module, "DATABASE_URL", candidate)
        base_url = candidate
      return session
    except Exception as exc:
      last_exc = exc
      log = LOGGER.error if is_last_attempt else LOGGER.warning
      log('Failed to initialize database engine with url %s: %s', candidate, exc)

  LOGGER.error(
      'Exiting because the database engine could not be initialized after trying %s.',
      candidates,
  )
  if last_exc:
    raise SystemExit(1) from last_exc
  raise SystemExit(1)


BASE = declarative_base()
SESSION = start()
