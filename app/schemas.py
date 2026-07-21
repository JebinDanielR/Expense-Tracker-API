from pydantic import BaseModel, Field
from datetime import date


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }

class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    description: str | None = None
    spent_on: date
    category_id: int


class ExpenseUpdate(BaseModel):
    amount: float = Field(gt=0)
    description: str | None = None
    spent_on: date
    category_id: int


class ExpenseResponse(BaseModel):
    id: int
    amount: float
    description: str | None
    spent_on: date
    category_id: int
    category_name: str

    model_config = {
        "from_attributes": True
    }