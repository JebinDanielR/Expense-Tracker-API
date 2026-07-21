from fastapi import APIRouter
from app.schemas import CategoryCreate, CategoryResponse, CategoryUpdate
from app.database import get_db
from app.models import Category
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends

router = APIRouter()


@router.get("/")
def home():
    return {
        "message": "Expense Tracker API"
    }

# GET /categories
@router.get(
    "/categories",
    response_model=list[CategoryResponse]
)
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


# GET /categories/{id}
@router.get(
    "/categories/{id}",
    response_model=CategoryResponse
)
def get_category(id: int, db: Session = Depends(get_db)):
    category = db.get(Category, id)

    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return category


# POST /categories
@router.post(
    "/categories",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
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
@router.put(
    "/categories/{id}",
    response_model=CategoryResponse
)
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
@router.delete(
    "/categories/{id}",
    status_code=status.HTTP_204_NO_CONTENT
)
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