from __future__ import annotations

from sqlalchemy import BigInteger, Integer, Text, Date, Numeric, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Project(Base):
    """프로젝트

    기존 DB(public.projects)를 그대로 매핑합니다.
    """

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    code: Mapped[str | None] = mapped_column(Text, nullable=True)
    name: Mapped[str] = mapped_column(Text)

    client_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("clients.id"))
    pm_user_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)

    # DB ENUM(public.project_status) (대문자 값 사용)
    status: Mapped[str] = mapped_column(
        ENUM(
            "PLANNING",
            "IN_PROGRESS",
            "ON_HOLD",
            "DONE",
            "CLOSED",
            name="project_status",
            create_type=False,
        ),
        default="PLANNING",
    )

    start_date: Mapped[object | None] = mapped_column(Date, nullable=True)
    due_date: Mapped[object | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[object | None] = mapped_column(Date, nullable=True)

    contract_amount: Mapped[object | None] = mapped_column(Numeric(14, 2), nullable=True)
    memo: Mapped[str | None] = mapped_column(Text, nullable=True)

    # v2 migration으로 추가된 컬럼
    department_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("departments.id"), nullable=True)
    business_type_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("project_business_types.id"), nullable=True)
    has_unread_update: Mapped[bool] = mapped_column(Boolean, default=False)
    admin_last_seen_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    admin_last_seen_by: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)

    created_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True))
    deleted_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)


class ProjectBusinessType(Base):
    __tablename__ = "project_business_types"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    memo: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True))
    deleted_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)


class ProjectUpdate(Base):
    __tablename__ = "project_updates"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("projects.id"))
    department_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("departments.id"), nullable=True)

    content: Mapped[str] = mapped_column(Text)

    created_by: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    created_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True))
    deleted_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)


class ProjectEvaluation(Base):
    __tablename__ = "project_evaluations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("projects.id"))
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    score: Mapped[object] = mapped_column(Numeric(4, 1))
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_by: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id"))
    created_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[object] = mapped_column(TIMESTAMP(timezone=True))
    deleted_at: Mapped[object | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
