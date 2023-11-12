import os
import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import (
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship
from src.infra.postgres.entity import Entity


class FoodItemEntity(Entity):
    __tablename__ = "food_item"
    __table_args__ = (
        ForeignKeyConstraint(
            ["donor_id"],
            [f'{os.getenv("POSTGRES_SCHEMA", "platable")}.donor.id'],
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
    
    donor_id = Column(
        Integer,
        index=True,
        nullable=False,
    )
    
    food_item_id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        index=True,
        unique=True,
    )
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
    description = Column(
        String,
        nullable=False
    )
    
    name = Column(
        String,
        index=True,
        nullable=False,
    )

    donor = relationship(
        "DonorEntity",
        back_populates="food_items",
        lazy="subquery",
        uselist=False,
    )

    batches = relationship(
        "BatchEntity",
        back_populates="food_item",
        lazy="subquery",
        uselist=True,
    )
