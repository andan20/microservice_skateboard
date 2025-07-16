from sqlmodel import Field, SQLModel


class Skateboards(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    number: int = Field(default=0, index=True)
    model: str | None = Field(default = None)
    color: str | None = Field(default = None)
    is_free: bool = Field(default=True)
    num_of_automat: int | None = Field(default=None)