import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Callable, Dict, List, Optional
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from src.infra.postgres.config import Config
from src.infra.postgres.repository import Repository


logger = logging.getLogger(__name__)


class UnitOfWork:
    def __init__(self, config: Config, repositories: Optional[List[Repository]] = None):
        repositories = repositories if repositories else []

        self.__config = config
        self.__engine = None
        self.__repositories: Dict[str, Repository] = {}

        for repository in repositories:
            self.__repositories.update({repository.__class__.__name__: repository})

    async def connect(self):
        if self.__engine:
            return

        connection_string = URL.create(
            database=self.__config.database,
            drivername=self.__config.drivername,
            host=self.__config.host,
            password=self.__config.password,
            port=self.__config.port,
            username=self.__config.username,
        )

        self.__engine = create_async_engine(
            url=connection_string,
            future=True,
            poolclass=NullPool,
        )

        self.__session_pool = asyncio.Queue(maxsize=self.__config.pool_size)

        for _ in range(0, self.__config.pool_size):
            await self.__session_pool.put(
                sessionmaker(
                    bind=self.__engine,
                    autoflush=False,
                    autocommit=False,
                    class_=AsyncSession,
                )()
            )

    @property
    def repositories(self) -> List[Repository]:
        return [value for key, value in self.__repositories.items()]

    @asynccontextmanager
    async def connection(self) -> AsyncConnection:
        if self.__engine is None:
            raise Exception("Database connection has not been established.")

        async_connection = AsyncConnection(async_engine=self.__engine)
        logger.info("Database connection established.")

        try:
            yield async_connection
            await async_connection.close()
        except Exception as exception:
            await async_connection.close()
            raise exception

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        if self.__engine is None:
            raise Exception("Database connection has not been established.")

        if self.__session_pool.empty():
            delay = 0

            while self.__session_pool.empty():
                delay = 0 if delay > 20 else delay
                delay += 5
                await asyncio.sleep(delay/10)
        
        current_session = await self.__session_pool.get()

        for repository in self.repositories:
            repository.session = current_session

        logger.info("Database session established.")
        
        try:
            yield current_session
        except Exception as exception:
            await current_session.close()

            await self.__session_pool.put(
                sessionmaker(
                    bind=self.__engine,
                    autoflush=False,
                    autocommit=False,
                    class_=AsyncSession,
                )()
            )

            raise exception
        
        await self.__session_pool.put(current_session)

    def add_repository(self, repository: Repository):
        self.__repositories.update({repository.__class__.__name__: repository})

    def get_repository(self, repository: Callable) -> Optional[Repository]:
        repository_instance = self.__repositories.get(repository.__name__)
        if isinstance(repository_instance, Repository):
            return repository_instance

        return None
