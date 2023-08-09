from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from keyvalue_sqlite import KeyValueSqlite

from sqlalchemy.orm import sessionmaker
from starlette.config import Config


config = Config('.env')
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')

SQLALCHEMY_ASYNC_DATABASE_URL = config('SQLALCHEMY_ASYNC_DATABASE_URL')

DB_PATH = config('DB_PATH')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


async_engine = create_async_engine(SQLALCHEMY_ASYNC_DATABASE_URL)

#DB_PATH = '/path/to/db.sqlite'

akv_db = KeyValueSqlite(DB_PATH, 'auth_key_value')




SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata = MetaData(naming_convention=naming_convention)

#@contextlib.contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    db = AsyncSession(bind=async_engine)
    try:
        yield db
    finally:
        await db.close()