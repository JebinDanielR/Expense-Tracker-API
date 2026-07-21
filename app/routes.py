from fastapi import APIRouter
from app.schemas import CategoryCreate, CategoryResponse, CategoryUpdate, ExpenseCreate, ExpenseResponse, ExpenseUpdate
from app.database import get_db
from app.models import Category,Expense
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status, Response, Depends
from datetime import date

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Expense Tracker API"
    }

# GET /categories
@router.get("/categories", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()

# GET /categories/{id}
@router.get("/categories/{id}",response_model=CategoryResponse)
def get_category(id: int, db: Session = Depends(get_db)):
    category = db.get(Category, id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return category

# POST /categories
@router.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    existing = (
        db.query(Category)
        .filter(Category.name == category.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists"
        )

    new_category = Category(name=category.name)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

# PUT /categories/{id}
@router.put("/categories/{id}", response_model=CategoryResponse)
def update_category(
    id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db)
):
    category = db.get(Category, id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    duplicate = (
        db.query(Category)
        .filter(
            Category.name == category_data.name,
            Category.id != id
        )
        .first()
    )

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category already exists"
        )

    category.name = category_data.name

    db.commit()
    db.refresh(category)

    return category

# DELETE /categories/{id}
@router.delete("/categories/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, db: Session = Depends(get_db)):
    category = db.get(Category, id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    if category.expenses:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete category because it has associated expenses."
        )

    db.delete(category)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

def expense_response(expense):
    return {
        "id": expense.id,
        "amount": expense.amount,
        "description": expense.description,
        "spent_on": expense.spent_on,
        "category_id": expense.category_id,
        "category_name": expense.category.name
    }

@router.get("/expenses", response_model=list[ExpenseResponse])
def get_expenses(
    category_id: int | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(Expense)

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

    return [
        expense_response(expense)
        for expense in expenses
    ]

@router.get("/expenses/{id}", response_model=ExpenseResponse)
def get_expense(
    id:int,
    db:Session=Depends(get_db)
):

    expense = db.get(Expense,id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense_response(expense)

@router.post("/expenses", response_model=ExpenseResponse, status_code=201)
def create_expense(
    expense_data: ExpenseCreate,
    db:Session=Depends(get_db)
):

    category = db.get(
        Category,
        expense_data.category_id
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    expense = Expense(
        amount=expense_data.amount,
        description=expense_data.description,
        spent_on=expense_data.spent_on,
        category_id=expense_data.category_id
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense_response(expense)

@router.put("/expenses/{id}", response_model=ExpenseResponse)
def update_expense(
    id:int,
    expense_data:ExpenseUpdate,
    db:Session=Depends(get_db)
):

    expense=db.get(Expense,id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    category=db.get(
        Category,
        expense_data.category_id
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    expense.amount=expense_data.amount
    expense.description=expense_data.description
    expense.spent_on=expense_data.spent_on
    expense.category_id=expense_data.category_id

    db.commit()
    db.refresh(expense)

    return expense_response(expense)

@router.delete("/expenses/{id}", status_code=204)
def delete_expense(
    id:int,
    db:Session=Depends(get_db)
):

    expense=db.get(Expense,id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()