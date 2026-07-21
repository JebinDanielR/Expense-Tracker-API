import strawberry
from datetime import date
from sqlalchemy.orm import joinedload

from ..database import SessionLocal
from ..models import Expense, Category

from .types import ExpenseType, CategoryType

@strawberry.type
class Query:

    @strawberry.field
    def hello(self) -> str:
        return "GraphQL working"

@strawberry.type
class Query:

    @strawberry.field
    def categories(self) -> list[CategoryType]:

        db = SessionLocal()
        categories = (
        db.query(Category)
        .options(
            joinedload(Category.expenses)
        )
        .all())    
        db.close()

        return categories

    @strawberry.field
    def expenses(
    self,
    category_id: int | None = None,
    from_date: date | None = None,
    to_date: date | None = None
    ) -> list[ExpenseType]:

        db = SessionLocal()

        query = (
        db.query(Expense)
        .options(
            joinedload(Expense.category)
        )
    )

        if category_id:
            query = query.filter(
                Expense.category_id == category_id
        )

        if from_date:
            query = query.filter(
            Expense.spent_on >= from_date
        )

        if to_date:
            query = query.filter(
            Expense.spent_on <= to_date
        )

        expenses = query.all()

        db.close()

        return expenses

schema = strawberry.Schema(
    query=Query
)