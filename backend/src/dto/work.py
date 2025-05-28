from src.dto.base import BaseDTO


class GetWorkResponseDTO(BaseDTO):
    id_work_scope: int
    work_name: str
    work_unit: str
    work_scope: int
