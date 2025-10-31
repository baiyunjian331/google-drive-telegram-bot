from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from bot import DATABASE_URL, LOGGER


def start() -> scoped_session:
    try:
        engine_kwargs = {"pool_pre_ping": True}
        url = make_url(DATABASE_URL)
        if url.drivername == 'sqlite':
            db_path = Path(url.database or "")
            if db_path:
                if not db_path.is_absolute():
                    db_path = Path.cwd() / db_path
                db_path.parent.mkdir(parents=True, exist_ok=True)
                url = url.set(database=str(db_path))
            engine_kwargs["connect_args"] = {"check_same_thread": False}
        engine = create_engine(url, **engine_kwargs)
        BASE.metadata.bind = engine
        BASE.metadata.create_all(engine)
        return scoped_session(sessionmaker(bind=engine, autoflush=False))
    except (OSError, SQLAlchemyError) as exc:
        LOGGER.error(
            'Failed to initialize database engine with url %s: %s', DATABASE_URL, exc
        )
        raise SystemExit(1) from exc


BASE = declarative_base()
SESSION = start()