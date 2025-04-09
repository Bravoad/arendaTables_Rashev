from typing import Optional
from pydantic import BaseModel


class TableBase(BaseModel):
    name: str
    seats: int
    location: Optional[str] = None


class TableCreate(TableBase):
    pass


class TableRead(TableBase):
    id: int

    class Config:
        orm_mode = True
