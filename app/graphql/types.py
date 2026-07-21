from __future__ import annotations

import strawberry
from datetime import date

@strawberry.type
class ExpenseType:
    id: int
    amount: float
    description: str | None
    spent_on: date
    category: CategoryType

@strawberry.type
class CategoryType:
    id: int
    name: str
    expenses: list[ExpenseType]