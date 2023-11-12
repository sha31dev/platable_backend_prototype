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


class DonationEntity(Entity):
    __tablename__ = "donation"
    __table_args__ = (
        ForeignKeyConstraint(
            ["batch_id"],
            [f'{os.getenv("POSTGRES_SCHEMA", "platable")}.batch.id'],
        ),
        ForeignKeyConstraint(
            ["recipient_id"],
            [f'{os.getenv("POSTGRES_SCHEMA", "platable")}.recipient.id'],
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

    donation_id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        index=True,
        unique=True,
    )

    batch_id = Column(
        Integer,
        index=True,
        nullable=False,
    )

    recipient_id = Column(
        Integer,
        index=True,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    quantity = Column(
        Integer,
        default=0,
        nullable=False,
    )

    batch = relationship(
        "BatchEntity",
        back_populates="donations",
        lazy="subquery",
        uselist=False,
    )

    recipient = relationship(
        "RecipientEntity",
        back_populates="donations",
        lazy="subquery",
        uselist=False,
    )
