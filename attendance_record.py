from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.sql import func

from app.models.base import Base


class AttendanceRecord(Base):
    """근태 확정(일자 귀속) 테이블.

    - work_sessions: 출퇴근 원천 로그(여러 세션 가능)
    - attendance_records: 일자/사용자 단위로 확정된 체크인/체크아웃 및 상태

    DB에는 enum 타입(attendance_status/shift_type)이 존재하지만,
    서버에서는 문자열로 다루어 호환성을 유지합니다.
    """

    __tablename__ = "attendance_records"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    work_date = Column(Date, nullable=False)
    work_date_basis = Column(Date, nullable=False)

    check_in_at = Column(DateTime(timezone=True))
    check_out_at = Column(DateTime(timezone=True))

    # DB enum: public.attendance_status (기본값 WORKING)
    status = Column(String, nullable=False, server_default="WORKING")

    note = Column(Text)

    created_by = Column(BigInteger)
    updated_by = Column(BigInteger)

    # DB enum: public.shift_type (기본값 DAY)
    shift_type = Column(String, nullable=False, server_default="DAY")

    is_holiday_work = Column(Boolean, nullable=False, server_default="false")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True))
