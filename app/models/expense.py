from datetime import datetime

from sqlalchemy import (
    Boolean,
    Integer,
    Float,
    DateTime,
    Column,
    String,
    ForeignKey
)

from app.core.db import Base


class Expense(Base):

    __tablename__ = "expenses"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    title = Column(
        String(50),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    show = Column(
        Boolean,
        default=True
    )

    amount = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )