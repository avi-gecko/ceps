from datetime import date, timedelta

from sqlalchemy import ForeignKey, String, Text, Date, Interval
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import MONEY
from decimal import Decimal


class BaseModel(DeclarativeBase):
    pass


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=False)


class WorkType(BaseModel):
    __tablename__ = "work_types"

    id_work_type: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    unit: Mapped[str] = mapped_column(String())

    work_scope: Mapped["WorkScope"] = relationship(
        back_populates="work_type", uselist=False
    )
    journal_complete_works: Mapped["JournalCompleteWorks"] = relationship(
        back_populates="work_type", uselist=False
    )


class WorkScope(BaseModel):
    __tablename__ = "work_scopes"

    id_work_scope: Mapped[int] = mapped_column(primary_key=True)
    scope: Mapped[int] = mapped_column()
    id_work_type_work_types: Mapped[int] = mapped_column(
        ForeignKey("work_types.id_work_type"), unique=True
    )

    work_type: Mapped["WorkType"] = relationship(
        back_populates="work_scope", uselist=False
    )
    estimate_calc: Mapped["EstimateCalc"] = relationship(
        back_populates="work_scope", uselist=False
    )
    accepted_works: Mapped["AcceptedWorks"] = relationship(
        back_populates="work_scope", uselist=False
    )
    needs_machines: Mapped[list["NeedsMachines"]] = relationship(
        back_populates="work_scope"
    )
    needs_materials: Mapped[list["NeedsMaterials"]] = relationship(
        back_populates="work_scope"
    )
    calendar: Mapped["Calendar"] = relationship(
        back_populates="work_scope", uselist=False
    )


class EstimateCalc(BaseModel):
    __tablename__ = "estimate_calcs"

    id_estimates_calc: Mapped[int] = mapped_column(primary_key=True)
    build_cost: Mapped[Decimal] = mapped_column(MONEY())
    montage_cost: Mapped[Decimal] = mapped_column(MONEY())
    equip_cost: Mapped[Decimal] = mapped_column(MONEY())
    other_cost: Mapped[Decimal] = mapped_column(MONEY())
    total_cost: Mapped[Decimal] = mapped_column(MONEY(), nullable=False)
    id_work_scope_work_scopes: Mapped[int] = mapped_column(
        ForeignKey("work_scopes.id_work_scope"), unique=True
    )

    work_scope: Mapped["WorkScope"] = relationship(
        back_populates="estimate_calc", uselist=False
    )
    accepted_works: Mapped["AcceptedWorks"] = relationship(
        back_populates="estimate_calc", uselist=False
    )


class JournalCompleteWorks(BaseModel):
    __tablename__ = "journal_complete_works"

    id_journal_complete_work: Mapped[int] = mapped_column(primary_key=True)
    justification: Mapped[str] = mapped_column(Text())
    total_work_scope: Mapped[int] = mapped_column(nullable=False)
    total_work_cost: Mapped[Decimal] = mapped_column(MONEY(), nullable=False)
    scope_start_year: Mapped[int] = mapped_column()
    cost_start_year: Mapped[Decimal] = mapped_column(MONEY())
    scope_month: Mapped[int] = mapped_column()
    cost_month: Mapped[Decimal] = mapped_column(MONEY())
    scope_end_year: Mapped[int] = mapped_column()
    cost_end_year: Mapped[Decimal] = mapped_column(MONEY())
    scope_remain: Mapped[int] = mapped_column(nullable=False)
    cost_remain: Mapped[Decimal] = mapped_column(MONEY(), nullable=False)
    id_work_type_work_types: Mapped[int] = mapped_column(
        ForeignKey("work_types.id_work_type"), unique=True
    )

    work_type: Mapped["WorkType"] = relationship(
        back_populates="journal_complete_works", uselist=False
    )
    accepted_works: Mapped["AcceptedWorks"] = relationship(
        back_populates="journal_complete_work", uselist=False
    )


class AcceptedWorks(BaseModel):
    __tablename__ = "accepted_works"

    id_accepted_work: Mapped[int] = mapped_column(primary_key=True)
    scope_begin: Mapped[int] = mapped_column(nullable=False)
    cost_begin: Mapped[Decimal] = mapped_column(MONEY(), nullable=False)
    solid_cost: Mapped[Decimal] = mapped_column(MONEY(), nullable=False)
    id_work_scope_work_scopes: Mapped[int] = mapped_column(
        ForeignKey("work_scopes.id_work_scope"), unique=True
    )
    id_journal_complete_work_journal_complete_works: Mapped[int] = mapped_column(
        ForeignKey("journal_complete_works.id_journal_complete_work"), unique=True
    )
    id_estimates_calc_estimate_calcs: Mapped[int] = mapped_column(
        ForeignKey("estimate_calcs.id_estimates_calc"), unique=True
    )

    work_scope: Mapped["WorkScope"] = relationship(
        back_populates="accepted_works", uselist=False
    )
    journal_complete_work: Mapped["JournalCompleteWorks"] = relationship(
        back_populates="accepted_works", uselist=False
    )
    estimate_calc: Mapped["EstimateCalc"] = relationship(
        back_populates="accepted_works", uselist=False
    )


class MachineType(BaseModel):
    __tablename__ = "machine_types"

    id_machine_type: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())

    having_machines: Mapped["HavingMachines"] = relationship(
        back_populates="machine_type", uselist=False
    )
    needs_machines: Mapped[list["NeedsMachines"]] = relationship(
        back_populates="machine_type"
    )


class HavingMachines(BaseModel):
    __tablename__ = "having_machines"

    id_having_machine: Mapped[int] = mapped_column(primary_key=True)
    count: Mapped[int] = mapped_column(nullable=False)
    id_machine_type_machine_types: Mapped[int] = mapped_column(
        ForeignKey("machine_types.id_machine_type"), unique=True
    )

    machine_type: Mapped["MachineType"] = relationship(
        back_populates="having_machines", uselist=False
    )


class NeedsMachines(BaseModel):
    __tablename__ = "needs_machines"

    id_needs_machine: Mapped[int] = mapped_column(primary_key=True)
    count: Mapped[int] = mapped_column(nullable=False)
    id_work_scope_work_scopes: Mapped[int] = mapped_column(
        ForeignKey("work_scopes.id_work_scope")
    )
    id_machine_type_machine_types: Mapped[int] = mapped_column(
        ForeignKey("machine_types.id_machine_type")
    )

    work_scope: Mapped["WorkScope"] = relationship(back_populates="needs_machines")
    machine_type: Mapped["MachineType"] = relationship(back_populates="needs_machines")


class MaterialType(BaseModel):
    __tablename__ = "material_types"

    id_material_type: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    unit: Mapped[str] = mapped_column(String())
    standard: Mapped[int] = mapped_column(nullable=False)

    needs_materials: Mapped[list["NeedsMaterials"]] = relationship(
        back_populates="material_type"
    )


class NeedsMaterials(BaseModel):
    __tablename__ = "needs_materials"

    id_needs_material: Mapped[int] = mapped_column(primary_key=True)
    count: Mapped[int] = mapped_column(nullable=False)
    id_material_type_material_types: Mapped[int] = mapped_column(
        ForeignKey("material_types.id_material_type")
    )
    id_work_scope_work_scopes: Mapped[int] = mapped_column(
        ForeignKey("work_scopes.id_work_scope")
    )

    material_type: Mapped["MaterialType"] = relationship(
        back_populates="needs_materials"
    )
    work_scope: Mapped["WorkScope"] = relationship(back_populates="needs_materials")


class Calendar(BaseModel):
    __tablename__ = "calendar"

    id_work: Mapped[int] = mapped_column(primary_key=True)
    worker_count: Mapped[int] = mapped_column(nullable=False)
    machines_count: Mapped[int] = mapped_column(nullable=False)
    duration: Mapped[timedelta] = mapped_column(Interval(), nullable=False)
    date_start: Mapped[date] = mapped_column(Date(), nullable=False)
    date_end: Mapped[date] = mapped_column(Date(), nullable=False)
    id_work_scope_work_scopes: Mapped[int] = mapped_column(
        ForeignKey("work_scopes.id_work_scope"), unique=True
    )

    work_scope: Mapped["WorkScope"] = relationship(
        back_populates="calendar", uselist=False
    )
