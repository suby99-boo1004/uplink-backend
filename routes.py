from fastapi import FastAPI

from app.modules.health.router import router as health_router
from app.modules.auth.router import router as auth_router
from app.modules.attendance.router import router as attendance_router
from app.modules.projects.router import router as projects_router
from app.modules.products.router import router as products_router
from app.modules.estimates.router import router as estimates_router
from app.modules.materials.router import router as materials_router
from app.modules.maintenance.router import router as maintenance_router
from app.modules.design.router import router as design_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.admin.router import router as admin_router
from app.modules.admin_staff.router import router as admin_staff_router
from app.modules.work_sessions.router import router as work_sessions_router
from app.modules.users.router import router as users_router
from app.modules.employees.router import router as employees_router


def include_routes(app: FastAPI) -> None:
    """모듈 라우터 등록(고정형)"""
    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(attendance_router)
    app.include_router(projects_router)
    app.include_router(estimates_router)
    app.include_router(materials_router)
    app.include_router(maintenance_router)
    app.include_router(design_router)
    app.include_router(dashboard_router)
    app.include_router(admin_router)
    app.include_router(admin_staff_router)  # ✅ 직원관리(직원 리포트)
    app.include_router(work_sessions_router)
    app.include_router(users_router)
    app.include_router(employees_router)

    # ✅ 제품(자재관리): router 내부에 prefix가 없으므로 여기서 '/api/products'를 고정
    app.include_router(products_router, prefix="/api/products", tags=["products"])
