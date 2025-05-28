from typing import Annotated, Sequence

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dto.user import UserResponse
from src.dto.work import GetWorkResponseDTO
from src.modules.auth.utils import get_current_active_user
from src.db.session import get_session
from src.db.models import WorkScope, WorkType

router = APIRouter(tags=["work"])


@router.get("/work-scope")
async def get_work_scopes(
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Sequence[GetWorkResponseDTO]:
    stmt = (
        select(
            WorkScope.id_work_scope,
            WorkType.name.label("work_name"),
            WorkType.unit.label("work_unit"),
            WorkScope.scope.label("work_scope"),
        )
        .select_from(WorkScope)
        .join(WorkType)
    )
    result = await session.execute(stmt)
    return result.mappings().all()
