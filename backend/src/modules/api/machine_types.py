from typing import Annotated, Sequence

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.dto.user import UserResponse
from src.modules.auth.utils import get_current_active_user
from src.db.session import get_session
from src.db.models import MachineType, HavingMachines
from src.dto.machine import MachineResponse

router = APIRouter(tags=["machine"])


@router.get("/machine", response_model=Sequence[MachineResponse])
async def get_machine_types(
    _: Annotated[UserResponse, Depends(get_current_active_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Sequence[MachineResponse]:
    result = await session.execute(select(
            MachineType.id_machine_type,
            MachineType.name,
            HavingMachines.count.label("count")
        )
        .join(HavingMachines, MachineType.having_machines, isouter=True)
    )
    machine_types = result.mappings().all()
    return machine_types
