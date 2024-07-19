import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from src.core.settings.config import settings
from src.todos.graphql.ouery import Query

app = FastAPI(
    title=f"{settings.APP_NAME}-{settings.RUN_ENV}",
    version=settings.VERSION,
    debug=settings.DEBUG or False,
)

schemas = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schemas)

app.add_route("/graphql", graphql_app)  # type: ignore
