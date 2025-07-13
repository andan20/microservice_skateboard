from sqlmodel import Field, SQLModel


class Wallet(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    username: str = Field(index=True, unique=True)
    balance: int = Field(default=0)
    is_ban: bool = Field(default=False)