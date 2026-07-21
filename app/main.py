from fastapi import FastAPI

from .database import Base, engine
from .routes import router

app = FastAPI(
    title="Expense Tracker API"
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


app.include_router(router)