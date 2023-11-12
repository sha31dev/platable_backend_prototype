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
from sqlalchemy.schema import PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from src.infra.postgres.entity import Entity


class DonorEntity(Entity):
    __tablename__ = "donor"
    __table_args__ = (
        PrimaryKeyConstraint("id"),
        {
            "schema": os.getenv(
                "POSTGRES_SCHEMA",
                "platable",
            ),
        }
    )

    id = Column(
        Integer,
        autoincrement=True,
        primary_key=True,
    )

    donor_id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        index=True,
        unique=True,
    )
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    contact = Column(
        String,
        index=True,
        nullable=False,
    )

    name = Column(
        String,
        index=True,
        nullable=False,
    )

    food_items = relationship(
        "DonorEntity",
        back_populates="donor",
        lazy="subquery",
        uselist=True,
    )
