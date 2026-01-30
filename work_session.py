from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.models.base import Base


class WorkSession(Base):
    __tablename__ = "work_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # OFFICE / OUTSIDE / TRIP_VIRTUAL / LEAVE
    session_type = Column(String(20), nullable=False)

    # DAY / NIGHT
    shift_type = Column(String(10), nullable=False)

    start_at = Column(DateTime(timezone=True), nullable=False)
    end_at = Column(DateTime(timezone=True))

    # 집계 기준일 (DAY=당일, NIGHT=다음날)
    work_date_basis = Column(Date, nullable=False)

    place = Column(String)
    task = Column(String)

    # 직원이 휴일근무 체크박스를 눌렀을 때만 True
    is_holiday = Column(Boolean, default=False)

    # manual / bulk / system 등
    source = Column(String(20), default="manual")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
