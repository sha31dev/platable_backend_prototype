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
from sqlalchemy.orm import relationship
from sqlalchemy.schema import PrimaryKeyConstraint
from src.infra.postgres.entity import Entity


class RecipientEntity(Entity):
    __tablename__ = "recipient"
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

    recipient_id = Column(
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

    donations = relationship(
        "DonationEntity",
        back_populates="recipient",
        lazy="subquery",
        uselist=True,
    )
