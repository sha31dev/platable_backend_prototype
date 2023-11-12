from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from src.infra.postgres import Repository
from src.infra.postgres.entities import DonorEntity


class DonorsRepository(Repository):
    def __init__(self, session: Optional[AsyncSession] = None):
        self.__session = session

    @property
    def session(self) -> AsyncSession:
        return self.__session

    @session.setter
    def session(self, session: AsyncSession):
        self.__session = session

    async def get_donor(self, filters: dict):
        return await super().select(
            entity=DonorEntity,
            filters=filters,
        )
