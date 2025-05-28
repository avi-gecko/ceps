from typing import List

from src.dto.base import BaseDTO


class MachineResponse(BaseDTO):
    machine_id: int
    machine_name: str
    count: int | None


class GetNeedsMachineResponseDTO(BaseDTO):
    id_work_scope: int
    work_name: str
    work_unit: str
    work_scope: int
    machines: List[MachineResponse]
