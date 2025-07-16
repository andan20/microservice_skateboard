from sqlmodel import Field, SQLModel
from datetime import datetime


class Rent(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    username: str = Field(index=True, unique=True)
    number: int = Field(index=True, unique=True)
    time_start: datetime = Field()