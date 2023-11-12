import uuid
from fastapi import Request
from fastapi.responses import JSONResponse
from src.infra.postgres import UnitOfWork
from src.infra.postgres.repositories import FoodItemsRepository
from src.util.exceptions import HttpException


class DeleteFoodItemController:
    path = "/food_items/{food_item_id}"
    methods = ["DELETE"]

    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work = unit_of_work

    async def handle(self, request: Request):
        food_item_id = request.path_params.get("food_item_id")
        filters = {"is_active": True, "food_item_id": food_item_id}

        if food_item_id:
            try:
                uuid.UUID(str(food_item_id))
            except Exception:
                raise HttpException(status=404, message="FoodItem not found.")

        async with self.__unit_of_work.session() as session:
            await session.begin()

            food_items_repository = self.__unit_of_work.get_repository(FoodItemsRepository)

            food_item_entity = await food_items_repository.get_food_item(
                filters=filters,
            )

            if food_item_entity is None:
                raise HttpException(status=404, message="FoodItem not found.")

            await food_items_repository.update_food_items(
                filters=filters, properties={"is_active": False}
            )

            await session.commit()

        return JSONResponse(
            content={"message": "Resource deleted."},
            status_code=200,
        )
