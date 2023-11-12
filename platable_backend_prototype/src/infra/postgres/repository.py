from abc import ABC
from typing import List, Optional
from sqlalchemy import func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import Executable
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.expression import delete
from sqlalchemy.future import select
from src.infra.postgres.entity import Entity


class Repository(ABC):
    def __init__(self, session: Optional[AsyncSession] = None):
        self.__session = session

    @property
    def session(self) -> AsyncSession:
        return self.__session

    @session.setter
    def session(self, session: AsyncSession):
        self.__session = session

    async def count(
        self,
        entity: Entity,
        filters: Optional[dict] = None,
    ) -> int:
        filters = filters if filters else {}
        query = select(func.count(text("*"))).select_from(select(entity).filter_by(**filters))
        count = await self.session.execute(query)
        return count.fetchone()[0]

    async def delete(
        self,
        entity: Entity,
        filters: Optional[dict] = None,
    ):
        filters = filters if filters else {}
        await self.session.execute(delete(entity).filter_by(**filters))

    async def execute(self, query: Executable):
        results = await self.session.execute(query)
        return results

    async def insert(
        self,
        entities: List[Entity],
        patch: bool = True,
    ):
        rows = []

        if len(entities) > 0:
            columns_to_remove = ["_sa_instance_state"]
            for key, value in entities[0].__dict__.copy().items():
                if isinstance(value, Entity):
                    columns_to_remove.append(key)

                if isinstance(value, List):
                    if all(isinstance(v, Entity) for v in value):
                        columns_to_remove.append(key)

            for entity in entities:
                properties = entity.__dict__.copy()

                for column in columns_to_remove:
                    properties.pop(column, None)

                rows.append(properties)

            results = await self.session.execute(
                insert(entities[0].__table__)
                .values(rows)
                .returning(type(entities[0]) if patch else None)
            )

            if patch:
                rows = [row for row in results.fetchall()]

                for index, row in enumerate(rows):
                    row = row._asdict()
                    for key in row.keys():
                        setattr(entities[index], key, row.get(key))

            await self.session.flush()

    async def select(
        self,
        entity: Entity,
        filters: Optional[dict] = None,
    ) -> Entity:
        filters = filters if filters else {}
        rows = await self.session.execute(select(entity).filter_by(**filters))

        try:
            return rows.fetchone()[0]
        except Exception:
            return None

    async def select_all(
        self,
        entity: Entity,
        filters: Optional[dict] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> List[Entity]:
        filters = filters if filters else {}
        rows = await self.session.execute(
            select(entity).filter_by(**filters).offset(offset).limit(limit)
        )
        return [row for row, in rows.fetchall()]

    async def update(
        self,
        entity: Entity,
        filters: Optional[dict] = None,
        properties: Optional[dict] = None,
    ):
        filters = filters if filters else {}
        properties = properties if properties else {}
        rows = await self.session.execute(select(entity).filter_by(**filters))
        rows = [row for row, in rows.fetchall()]

        for row in rows:
            for key, value in properties.items():
                setattr(row, key, value)

    async def upsert(
        self,
        entities: List[Entity],
        index_elements: List[str],
        update: bool = True,
        patch: bool = True,
        columns_to_update: Optional[List[str]] = None,
    ):
        rows = []

        if len(entities) > 0:
            columns_to_remove = ["_sa_instance_state"]
            columns_to_update = (
                columns_to_update if columns_to_update else list(entities[0].__dict__.copy().keys())
            )

            for key, value in entities[0].__dict__.copy().items():
                if isinstance(value, Entity):
                    columns_to_remove.append(key)

                if isinstance(value, List):
                    if all(isinstance(v, Entity) for v in value):
                        columns_to_remove.append(key)

            for entity in entities:
                properties = entity.__dict__.copy()

                for column in columns_to_remove:
                    properties.pop(column, None)

                    if column in columns_to_update:
                        columns_to_update.remove(column)

                if update:
                    for column in index_elements:
                        if column in columns_to_update:
                            columns_to_update.remove(column)

                rows.append(properties)

            query = (
                insert(entities[0].__table__)
                .values(rows)
                .returning(type(entities[0]) if patch else None)
            )

            if update:
                query = query.on_conflict_do_update(
                    index_elements=index_elements,
                    set_={column: getattr(query.excluded, column) for column in columns_to_update},
                )
            else:
                query = query.on_conflict_do_nothing(index_elements=index_elements)

            results = await self.session.execute(query)

            if patch:
                rows = [row for row in results.fetchall()]

                for index, row in enumerate(rows):
                    row = row._asdict()
                    for key in row.keys():
                        setattr(entities[index], key, row.get(key))

            await self.session.flush()
