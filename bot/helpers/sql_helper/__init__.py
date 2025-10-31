import os
from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from bot import DATABASE_URL, LOGGER


def start() -> scoped_session:
    try:
        engine_kwargs = {}
        url = make_url(DATABASE_URL)
        if url.drivername == 'sqlite':
            # Ensure parent directory exists when using a filesystem SQLite DB.
            db_path = url.database or ''
            db_dir = os.path.dirname(db_path)
            if db_path and db_dir and not os.path.isdir(db_dir):
                os.makedirs(db_dir, exist_ok=True)
            engine_kwargs["connect_args"] = {"check_same_thread": False}
        engine_kwargs["pool_pre_ping"] = True
        engine = create_engine(DATABASE_URL, **engine_kwargs)
        BASE.metadata.bind = engine
        BASE.metadata.create_all(engine)
        return scoped_session(sessionmaker(bind=engine, autoflush=False))
    except Exception as exc:
        LOGGER.error('Failed to initialize database engine with url %s: %s', DATABASE_URL, exc)
        exit(1)


BASE = declarative_base()
SESSION = start()