from fastapi import FastAPI

from .database import Base, engine
from .routes import router

from strawberry.fastapi import GraphQLRouter
from .graphql.schema import schema

app = FastAPI(
    title="Expense Tracker API"
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(router)



graphql_app = GraphQLRouter(schema)

app.include_router(
    graphql_app,
    prefix="/graphql"
)