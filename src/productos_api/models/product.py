from typing import Optional

from sqlmodel import SQLModel, Field


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    description: str | None = None
    price: float
    stock: int = 0