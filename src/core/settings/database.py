from asyncio import current_task
from collections.abc import AsyncGenerator

# from injector import provider
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from src.core.settings.config import settings
from src.core.settings.logs.logger import get_logger

logger = get_logger(__name__)

# enginとsessionの作成
try:
    engine = create_async_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
    )

    async_session_factory = async_scoped_session(
        async_sessionmaker(
            engine,
            autocommit=False,
            autoflush=False,
        ),
        scopefunc=current_task,
    )
except Exception as err:
    logger.error(f"DB connection failed. detail:{str(err)}")


# @provider
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    async_scoped_sessionはスレッドローカルではない
    そのため、scope_func（コールバック）にセッションのIDを返すことで、
    どのスレッド（スコープ）で実行するか指定する必要がある
    current_task()はasyncioの機能で現在のタスク自身のIDを返す
    それによりスレッドローカルと同じ接続ができるようになる
    """

    async with async_session_factory() as session:
        if async_session_factory is None:
            raise RuntimeError("AsyncScopedSession is not initialized")

        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()
