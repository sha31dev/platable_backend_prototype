from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from src.infra.postgres import Repository
from src.infra.postgres.entities import FoodItemEntity


class FoodItemsRepository(Repository):
    def __init__(self, session: Optional[AsyncSession] = None):
        self.__session = session

    @property
    def session(self) -> AsyncSession:
        return self.__session

    @session.setter
    def session(self, session: AsyncSession):
        self.__session = session

    async def insert_food_items(self, food_item_entities: List[FoodItemEntity]):
        return await super().insert(
            entities=food_item_entities,
            patch=True,
        )

    async def get_food_item(self, filters: dict):
        return await super().select(entity=FoodItemEntity, filters=filters)

    async def get_food_items(self, filters: dict, offset=0, limit=10):
        return await super().select_all(
            entity=FoodItemEntity,
            filters=filters,
            offset=offset,
            limit=limit,
        )

    async def update_food_items(self, filters: dict, properties: dict):
        await super().update(
            entity=FoodItemEntity,
            filters=filters,
            properties=properties,
        )
