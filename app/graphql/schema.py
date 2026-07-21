import strawberry


@strawberry.type
class Query:

    @strawberry.field
    def hello(self) -> str:
        return "GraphQL working"


schema = strawberry.Schema(
    query=Query
)