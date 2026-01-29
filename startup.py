from app.core.db import SessionLocal
from app.seed.create_admin import run_seed


def startup_seed() -> None:
    """서버 시작 시 초기 roles/관리자 계정 보장"""
    db = SessionLocal()
    try:
        run_seed(db)
        db.commit()
        print("[Uplink Seed] roles/admin seed OK")
    except Exception as e:
        db.rollback()
        print(f"[Uplink Seed] seed failed: {e}")
    finally:
        db.close()
