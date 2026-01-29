from __future__ import annotations

import os
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.core.startup import startup_seed
from app.core.routes import include_routes
from app.modules.admin_attendance.scheduler import start_scheduler


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    # CORS
    origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", include_in_schema=False)
    def root():
        html = """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Uplink</title>
  <style>
    body{font-family:system-ui,Segoe UI,Apple SD Gothic Neo,Malgun Gothic,sans-serif;padding:24px;line-height:1.5;}
    code{background:#f5f5f5;padding:2px 6px;border-radius:6px;}
    .box{max-width:720px;margin:0 auto;border:1px solid #e6e6e6;border-radius:14px;padding:18px;}
    h1{margin:0 0 10px 0;font-size:22px;}
    ul{margin:8px 0 0 18px;}
  </style>
</head>
<body>
  <div class="box">
    <h1>Uplink 백엔드가 정상 실행 중입니다 ✅</h1>
    <div>다음 주소로 기능을 확인할 수 있습니다.</div>
    <ul>
      <li>API 문서: <code>/docs</code></li>
      <li>헬스체크: <code>/api/health</code></li>
      <li>로그인: <code>POST /api/auth/login</code></li>
      <li>내 정보: <code>GET /api/auth/me</code></li>
    </ul>
    <p style="margin-top:12px;">
      ※ 실제 업링크의 <b>첫 화면(로그인 UI)</b>은 다음 단계에서 <b>프론트엔드(React)</b>로 구현합니다.
    </p>
  </div>
</body>
</html>"""
        return HTMLResponse(html)

    @app.on_event("startup")
    def _startup() -> None:
        # ✅ Seed는 반드시 유지 (고정형)
        startup_seed()

        # ✅ 자동퇴근 스케줄러는 웹페이지와 무관하게 백엔드 startup에서 항상 기동
        # ✅ 안정화: reload 환경에서 reloader/worker 중복 기동 가능성 완화(있으면 적용)
        try:
            # 일부 환경변수는 없을 수 있음(없으면 그냥 진행)
            for key in ("RUN_MAIN", "WERKZEUG_RUN_MAIN", "UVICORN_RUN_MAIN"):
                v = os.environ.get(key)
                if v is not None and v.lower() in ("false", "0", "no"):
                    return

            start_scheduler()
        except Exception:
            logging.getLogger("admin_attendance.scheduler").exception(
                "failed to start admin_attendance scheduler on startup"
            )

    # ✅ 라우터 등록도 고정형 함수로 분리
    include_routes(app)

    return app


app = create_app()
