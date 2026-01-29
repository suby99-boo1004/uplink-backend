from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 앱 기본 설정
    APP_NAME: str = "Uplink API"
    ENV: str = "local"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # DB 설정
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_SCHEMA: str = "public"

    # CORS (프론트 도메인)
    CORS_ORIGINS: str = "http://localhost:3000"

    # 운영 보안: 에러 상세 노출 여부
    # - local/dev: True 권장
    # - prod: False 권장
    # 미지정(None)이면 ENV 값에 따라 자동 결정합니다.
    SHOW_ERROR_DETAILS: bool | None = None
    
    # 초기 관리자(Seed)
    ADMIN_EMAIL: str = "admin@uplink.local"
    ADMIN_PASSWORD: str = "savein!2"
    ADMIN_NAME: str = "대표"


    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"

    @property
    def show_error_details(self) -> bool:
        # 명시값이 있으면 그 값을 우선
        if self.SHOW_ERROR_DETAILS is not None:
            return bool(self.SHOW_ERROR_DETAILS)
        env = (self.ENV or "").lower().strip()
        return env in {"local", "dev", "development"}


settings = Settings()
