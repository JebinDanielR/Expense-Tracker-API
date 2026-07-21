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

@strawberry.input
class ExpenseInput:

    amount: float
    description: str
    spent_on: date
    category_id: int

@strawberry.type
class Mutation:

    @strawberry.mutation
    def add_expense(
        self,
        input: ExpenseInput
    ) -> ExpenseType:

        db = SessionLocal()

        category = db.get(
            Category,
            input.category_id
        )

        if category is None:
            raise Exception(
                "Category not found"
            )

        expense = Expense(
            amount=input.amount,
            description=input.description,
            spent_on=input.spent_on,
            category_id=input.category_id
        )

        db.add(expense)
        db.commit()

        expense_id = expense.id

        db.close()

        db = SessionLocal()

        expense = (
            db.query(Expense)
            .options(
                joinedload(Expense.category)
            )
            .filter(
                Expense.id == expense_id
            )
            .first()
        )

        db.close()

        return expense

    @strawberry.mutation
    def delete_expense(
        self,
        id:int
    ) -> bool:

        db = SessionLocal()

        expense = db.get(
            Expense,
            id
        )

        if expense is None:
            raise Exception(
                "Expense not found"
            )

        db.delete(expense)
        db.commit()

        db.close()

        return True

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)