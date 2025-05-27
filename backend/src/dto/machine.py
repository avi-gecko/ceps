from pydantic import BaseModel


class MachineResponse(BaseModel):
    id_machine_type: int
    name: str
    count: int | None

    class Config:
        from_attributes = True
