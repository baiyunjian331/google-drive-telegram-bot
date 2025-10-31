import os
from typing import Optional

import bot
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from bot import LOGGER, DEFAULT_DATA_DIR


DATABASE_URL = bot.DATABASE_URL


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
  candidate_urls = [bot.DATABASE_URL]
  fallback_url = _sqlite_fallback_url(bot.DATABASE_URL)
  if fallback_url:
    candidate_urls.append(fallback_url)

  last_exc: Optional[Exception] = None
  for idx, candidate in enumerate(candidate_urls):
    is_last_attempt = idx == len(candidate_urls) - 1
    try:
      session = _create_session(candidate)
      if candidate != bot.DATABASE_URL:
        LOGGER.warning(
            'DATABASE_URL "%s" is not writable. Falling back to "%s".',
            bot.DATABASE_URL,
            candidate,
        )
        bot.DATABASE_URL = candidate
        globals()['DATABASE_URL'] = candidate
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
