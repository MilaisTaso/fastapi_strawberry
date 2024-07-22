import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from src.core.dependeny import get_context
from src.core.settings.config import settings
from src.todos.graphql.mutation import Mutation
from src.todos.graphql.query import Query

app = FastAPI(
    title=f"{settings.APP_NAME}-{settings.RUN_ENV}",
    version=settings.VERSION,
    debug=settings.DEBUG or False,
)

schemas = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schemas, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql")
