import os
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import (
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship
from src.infra.postgres.entity import Entity


class BatchEntity(Entity):
    __tablename__ = "batch"
    __table_args__ = (
        ForeignKeyConstraint(
            ["food_item_id"],
            [f'{os.getenv("POSTGRES_SCHEMA", "platable")}.food_item.id'],
            ondelete="cascade",
        ),
        PrimaryKeyConstraint("id"),
        {
            "schema": os.getenv(
                "POSTGRES_SCHEMA",
                "platable",
            ),
        },
    )

    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True,
    )

    batch_id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        index=True,
        unique=True,
    )
    
    food_item_id = Column(
        Integer,
        index=True,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    expiry_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    quantity = Column(
        Integer,
        default=0,
        nullable=False,
    )

    donations = relationship(
        "BatchEntity",
        back_populates="batch",
        lazy="subquery",
        uselist=True,
    )

    food_item = relationship(
        "FoodItemEntity",
        back_populates="batches",
        lazy="subquery",
        uselist=False,
    )
