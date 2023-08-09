from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from keyvalue_sqlite import KeyValueSqlite

from sqlalchemy.orm import sessionmaker
from starlette.config import Config
import os
from dotenv import load_dotenv
import redis


config = Config('.env')
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')

SQLALCHEMY_ASYNC_DATABASE_URL = config('SQLALCHEMY_ASYNC_DATABASE_URL')

DB_PATH = config('DB_PATH')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


def redis_config() :
    try:
        REDIS_HOST = config("REDIS_HOST")
        REDIS_PORT = int(config("REDIS_PORT"))
        REDIS_DATABASE = int(config("REDIS_DATABASE"))
        return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE)
        # redis.StrictRedis( ... ) 라고도 사용할 수 있다
        # Python의 버전이 3으로 업데이트 되면서 함수명이 변경되었다
        # 하지만 버전 호환을 위해 StrictRedis로도 연결을 할 수 있다
        # 즉, Redis = StrictRedis로 동일한 기능을 하는 함수이다
		
    except:
        print("redis connection failure")


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