from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .database import Base, engine
from .routes import router
from .graphql.schema import schema

from strawberry.fastapi import GraphQLRouter

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# REST routes
app.include_router(router)

# GraphQL route
graphql_app = GraphQLRouter(schema)
app.include_router(
    graphql_app,
    prefix="/graphql"
)

# Serve frontend files
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

# Frontend entry point
@app.get("/")
@app.get("/expense-tracker")
def home():
    return FileResponse(
        "app/static/index.html"
    )
