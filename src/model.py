from enum import Enum
from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column, Mapped

from database import Base


class Status(str, Enum):
    WAITING = "В ожидании"
    SEARCH = "В поиске"
    CHAT = "В чате"


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str | None] = mapped_column()
    name: Mapped[str | None] = mapped_column()

    status: Mapped[Status] = mapped_column(default=Status.WAITING)
    current_chat: Mapped[int | None] = mapped_column(BigInteger, unique=True)
