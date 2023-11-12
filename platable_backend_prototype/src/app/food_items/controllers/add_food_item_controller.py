import uuid
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.infra.postgres import UnitOfWork
from src.infra.postgres.entities import FoodItemEntity
from src.infra.postgres.repositories import (
    DonorsRepository,
    FoodItemsRepository,
)
from src.util.exceptions import HttpException


class AddFoodItemController:
    path = "/food_items"
    methods = ["POST"]

    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work = unit_of_work

    async def handle(self, request: Request):
        request_body = await request.json()

        try:
            uuid.UUID(str(request_body.get("donor_id")))
        except Exception:
            raise HttpException(status=404, message="Donor not found.")

        async with self.__unit_of_work.session() as session:
            await session.begin()

            donors_repository = self.__unit_of_work.get_repository(DonorsRepository)
            food_items_repository = self.__unit_of_work.get_repository(FoodItemsRepository)

            donor_entity = await donors_repository.get_donor(
                filters={
                    "donor_id": request_body.get("donor_id"),
                },
            )

            if donor_entity is None:
                raise HttpException(status=404, message="Donor not found.")

            food_item_entity = FoodItemEntity(
                donor_id=donor_entity.id,
                description=request_body.get("description", ""),
                name=request_body.get("name"),
            )

            await food_items_repository.insert_food_items(
                food_item_entities=[food_item_entity],
            )

            await session.commit()

        return JSONResponse(
            content={"message": "Resource created."},
            status_code=201,
        )
