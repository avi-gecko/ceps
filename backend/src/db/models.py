from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class User(BaseModel):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
