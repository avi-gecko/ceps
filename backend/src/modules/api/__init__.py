from src.modules.api.auth import router as auth_router
from src.modules.api.machine_api import router as machine_types_router
from src.modules.api.work_api import router as work_router

__all__ = (
    "auth_router",
    "machine_types_router",
    "work_router",
)
