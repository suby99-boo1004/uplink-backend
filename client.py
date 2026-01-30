from __future__ import annotations

from sqlalchemy import BigInteger, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Client(Base):
    """발주처(Clients)

    DB: public.clients
    """

    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(Text, default="client")

    contact_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    contact_phone: Mapped[str | None] = mapped_column(Text, nullable=True)
    contact_email: Mapped[str | None] = mapped_column(Text, nullable=True)
    memo: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True))
    deleted_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
