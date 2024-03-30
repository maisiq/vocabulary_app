import logging
import os

from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from fastapi.exceptions import HTTPException
from fastapi import status

engine = create_async_engine(
    os.environ.get('DB_URI', None),
    pool_size=5,
    max_overflow=10,
    echo=True
)


async def get_session():
    try:
        session = async_sessionmaker(engine)()
        yield session
    except OperationalError as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    finally:
        await session.close()


class Base(DeclarativeBase):
    metadata = MetaData(schema='words')
    type_annotation_map = {}
