from datetime import datetime
from zoneinfo import ZoneInfo

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


def india_time():
    return datetime.now(ZoneInfo("Asia/Kolkata"))


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

    amount = Column(
        Float,
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    category = Column(
        String(30),
        nullable=False,
        default="Other"
    )

    show = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        default=india_time
    )