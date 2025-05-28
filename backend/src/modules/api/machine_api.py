from typing import Annotated, Sequence

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dto.user import UserResponse
from src.modules.auth.utils import get_current_active_user
from src.db.session import get_session
from src.db.models import (
    MachineType,
    HavingMachines,
    NeedsMachines,
    WorkScope,
    WorkType,
)
from src.dto.machine import MachineResponse, GetNeedsMachineResponseDTO

router = APIRouter(tags=["machine"])


@router.get("/machine", response_model=Sequence[MachineResponse])
async def get_machine_types(
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Sequence[MachineResponse]:
    result = await session.execute(
        select(
            MachineType.id_machine_type.label("machine_id"),
            MachineType.name.label("machine_name"),
            HavingMachines.count.label("count"),
        ).join(HavingMachines, MachineType.having_machines, isouter=True)
    )
    return result.mappings().all()


@router.get("/needs-machine")
async def get_needs_machine(
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Sequence[GetNeedsMachineResponseDTO]:
    stmt = (
        select(
            WorkScope.id_work_scope.label("id_work_scope"),
            WorkType.name.label("work_name"),
            WorkType.unit.label("work_unit"),
            WorkScope.scope.label("work_scope"),
            func.json_agg(
                func.json_build_object(
                    "machine_id",
                    MachineType.id_machine_type,
                    "machine_name",
                    MachineType.name,
                    "count",
                    NeedsMachines.count,
                )
            ).label("machines"),
        )
        .select_from(NeedsMachines)
        .join(MachineType, NeedsMachines.machine_type)
        .join(WorkScope, NeedsMachines.work_scope)
        .join(WorkType, WorkScope.work_type)
        .group_by(
            WorkScope.id_work_scope, WorkType.name, WorkType.unit, WorkScope.scope
        )
    )

    result = await session.execute(stmt)
    return result.mappings().all()
