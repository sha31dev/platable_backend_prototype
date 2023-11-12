import uuid
from datetime import datetime
from starlette.requests import Request
from starlette.responses import JSONResponse
from src.infra.postgres import UnitOfWork
from src.infra.postgres.repositories import (
    DonorsRepository,
    FoodItemsRepository,
)
from src.util.exceptions import HttpException


class ListFoodItemsController:
    path = "/food_items"
    methods = ["GET"]

    def __init__(self, unit_of_work: UnitOfWork):
        self.__unit_of_work = unit_of_work

    async def handle(self, request: Request):
        donor_id = request.query_params.get("donor_id")
        filters = {"is_active": True}

        if donor_id:
            try:
                uuid.UUID(str(donor_id))
            except Exception:
                raise HttpException(status=404, message="Donor not found.")

        results = []
        async with self.__unit_of_work.session() as session:
            await session.begin()

            donors_repository = self.__unit_of_work.get_repository(DonorsRepository)
            food_items_repository = self.__unit_of_work.get_repository(FoodItemsRepository)

            if donor_id:
                donor_entity = await donors_repository.get_donor(
                    filters={"donor_id": donor_id},
                )

                if donor_entity is None:
                    raise HttpException(status=404, message="Donor not found.")

                filters.update({"donor_id": donor_entity.id})

            food_item_entities = await food_items_repository.get_food_items(
                filters=filters,
            )

            for food_item_entity in food_item_entities:
                results.append(
                    {
                        "food_item_id": str(food_item_entity.food_item_id),
                        "donor_id": str(food_item_entity.donor.donor_id),
                        "name": food_item_entity.name,
                        "description": food_item_entity.description,
                        "created_at": datetime.strftime(
                            food_item_entity.created_at, "%Y-%m-%dT%H:%M:%S"
                        ),
                        "batches": [
                            {
                                "batch_id": str(batch_entity.batch_id),
                                "created_at": datetime.strftime(
                                    batch_entity.created_at, "%Y-%m-%dT%H:%M:%S"
                                ),
                                "expiry_at": datetime.strftime(
                                    batch_entity.expiry_at, "%Y-%m-%dT%H:%M:%S"
                                ),
                                "quantity": batch_entity.quantity,
                            }
                            for batch_entity in food_item_entity.batches
                        ],
                    }
                )

            await session.commit()

        return JSONResponse(
            content={"data": results},
            status_code=200,
        )
