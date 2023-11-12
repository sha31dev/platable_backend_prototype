import asyncio
import os
import sys
from importlib import import_module


async def main():
    directory = os.path.dirname(os.path.realpath(__file__))
    root_directory = os.path.abspath(os.path.join(directory, os.pardir))
    sys.path.insert(0, root_directory)

    postgres = import_module("src.infra.postgres")

    config = postgres.Config(
        database=os.getenv("POSTGRES_DATABASE", "platable"),
        drivername=os.getenv("POSTGRES_DRIVERNAME", "postgresql+asyncpg"),
        host=os.getenv("POSTGRES_HOST", "172.10.0.2"),
        password=os.getenv("POSTGRES_PASSWORD", "Eos32Ty8"),
        port=os.getenv("POSTGRES_PORT", 5432),
        username=os.getenv("POSTGRES_USERNAME", "postgres"),
    )

    repositories = import_module("src.infra.postgres.repositories")

    unit_of_work = postgres.UnitOfWork(
        config=config,
        repositories=[
            repositories.DonorsRepository(),
            repositories.FoodItemsRepository(),
        ],
    )

    await unit_of_work.connect()

    food_items_controllers = import_module("src.app.food_items.controllers")

    server = import_module("src.server").Server(
        controllers=[
            food_items_controllers.AddFoodItemController(unit_of_work=unit_of_work),
            food_items_controllers.DeleteFoodItemController(unit_of_work=unit_of_work),
            food_items_controllers.ListFoodItemsController(unit_of_work=unit_of_work),
            food_items_controllers.UpdateFoodItemController(unit_of_work=unit_of_work),
        ]
    )

    server.start()


if __name__ == "__main__":
    asyncio.run(main())
