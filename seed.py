from datetime import date

from app.database import SessionLocal, Base, engine
from app.models import Category, Expense

Base.metadata.create_all(bind=engine)

db = SessionLocal()

db.query(Expense).delete()
db.query(Category).delete()

categories = [
    Category(name="Food"),
    Category(name="Transport"),
    Category(name="Rent"),
    Category(name="Fun"),
    Category(name="Shopping"),
]

db.add_all(categories)
db.commit()

categories = db.query(Category).all()

lookup = {c.name: c for c in categories}

expenses = [
    Expense(
        amount=12.5,
        description="Lunch",
        spent_on=date(2026, 6, 2),
        category=lookup["Food"]
    ),
    Expense(
        amount=6,
        description="Bus",
        spent_on=date(2026, 6, 3),
        category=lookup["Transport"]
    ),
    Expense(
        amount=950,
        description="June Rent",
        spent_on=date(2026, 6, 1),
        category=lookup["Rent"]
    ),
    Expense(
        amount=25,
        description="Movie",
        spent_on=date(2026, 6, 12),
        category=lookup["Fun"]
    ),
    Expense(
        amount=70,
        description="Shoes",
        spent_on=date(2026, 6, 15),
        category=lookup["Shopping"]
    ),
    Expense(
        amount=15,
        description="Dinner",
        spent_on=date(2026, 7, 3),
        category=lookup["Food"]
    ),
    Expense(
        amount=8,
        description="Metro",
        spent_on=date(2026, 7, 4),
        category=lookup["Transport"]
    ),
    Expense(
        amount=950,
        description="July Rent",
        spent_on=date(2026, 7, 1),
        category=lookup["Rent"]
    ),
    Expense(
        amount=30,
        description="Bowling",
        spent_on=date(2026, 7, 8),
        category=lookup["Fun"]
    ),
    Expense(
        amount=100,
        description="Headphones",
        spent_on=date(2026, 7, 9),
        category=lookup["Shopping"]
    ),
    Expense(
        amount=20,
        description="Coffee",
        spent_on=date(2026, 7, 10),
        category=lookup["Food"]
    ),
    Expense(
        amount=5,
        description="Taxi",
        spent_on=date(2026, 7, 11),
        category=lookup["Transport"]
    ),
]

db.add_all(expenses)
db.commit()
db.close()

print("Database seeded successfully.")