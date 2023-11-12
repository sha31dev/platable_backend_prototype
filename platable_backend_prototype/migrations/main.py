import asyncio
import json
import os
import sys
from datetime import datetime
from importlib import import_module
from sqlalchemy.schema import CreateSchema


async def main():
    directory = os.path.dirname(os.path.realpath(__file__))
    root_directory = os.path.abspath(os.path.join(directory, os.pardir))
    sys.path.insert(0, root_directory)

    postgres = import_module("src.infra.postgres")

    config = postgres.Config(
        database=os.getenv("POSTGRES_DATABASE", "platable"),
        drivername=os.getenv("POSTGRES_DRIVERNAME", "postgresql+asyncpg"),
        host=os.getenv("POSTGRES_DATABASE", "172.10.0.2"),
        password=os.getenv("POSTGRES_PASSWORD", "Eos32Ty8"),
        port=os.getenv("POSTGRES_PORT", 5432),
        username=os.getenv("POSTGRES_USERNAME", "postgres"),
    )

    schema = os.getenv("POSTGRES_SCHEMA", "platable")
    unit_of_work = postgres.UnitOfWork(config=config)

    await unit_of_work.connect()

    async with unit_of_work.connection() as connection:
        await connection.start()
        await connection.execute(CreateSchema(schema))
        await connection.run_sync(postgres.Entity.metadata.create_all)

        directory = os.path.dirname(os.path.abspath(__file__))
        
        file = f"{directory}/dumps/donors.json"
        with open(file=file, encoding="utf-8") as file:
            await connection.execute(
                postgres.entities.DonorEntity.__table__.insert(),
                json.load(file),
            )

        file = f"{directory}/dumps/food_items.json"
        with open(file=file, encoding="utf-8") as file:
            await connection.execute(
                postgres.entities.FoodItemEntity.__table__.insert(),
                json.load(file),
            )

        file = f"{directory}/dumps/batches.json"
        with open(file=file, encoding="utf-8") as file:
            rows = json.load(file)
            for row in rows:
                row.update({
                    "expiry_at": datetime.strptime(
                        row.get("expiry_at"),
                        "%Y-%m-%dT%H:%M:%S",
                    ),
                })

            await connection.execute(
                postgres.entities.BatchEntity.__table__.insert(),
                rows,
            )

        file = f"{directory}/dumps/recipients.json"
        with open(file=file, encoding="utf-8") as file:
            await connection.execute(
                postgres.entities.RecipientEntity.__table__.insert(),
                json.load(file),
            )

        file = f"{directory}/dumps/donations.json"
        with open(file=file, encoding="utf-8") as file:
            rows = json.load(file)
            for row in rows:
                row.update({
                    "created_at": datetime.strptime(
                        row.get("created_at"),
                        "%Y-%m-%dT%H:%M:%S",
                    ),
                })
            
            await connection.execute(
                postgres.entities.DonationEntity.__table__.insert(),
                rows,
            )

        await connection.commit()


if __name__ == "__main__":
    asyncio.run(main())
