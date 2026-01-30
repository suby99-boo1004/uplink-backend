from sqlalchemy import BigInteger, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    email: Mapped[str] = mapped_column(Text)
    password_hash: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(Text)

    role_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("roles.id"))
    department_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("departments.id"), nullable=True)

    status: Mapped[str] = mapped_column(Text)
    last_login_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
