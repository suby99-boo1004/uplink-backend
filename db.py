from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        # 기본 public이지만, 명시적으로 검색 경로를 잡아두면 안전합니다.
        db.execute(text(f"SET search_path TO {settings.DB_SCHEMA};"))
        yield db
    finally:
        db.close()
