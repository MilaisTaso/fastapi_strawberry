import strawberry
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from src.auth.api import auth
from src.core.dependencies import get_context
from src.core.settings.config import settings
from src.todos.graphql.mutation import TodoMutation
from src.todos.graphql.query import TodoQuery


@strawberry.type
class Query(TodoQuery):
    pass


@strawberry.type
class Mutation(TodoMutation):
    pass


app = FastAPI(
    title=f"{settings.APP_NAME}-{settings.RUN_ENV}",
    version=settings.VERSION,
    debug=settings.DEBUG or False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.ORIGIN_RESOURCES],
    allow_origin_regex=r"^https?:\/\/([\w\-\_]{1,}\.|)example\.com",
    allow_methods=["*"],
    allow_headers=["*"],
)

schemas = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schemas, context_getter=get_context)

app.include_router(router=auth.router, prefix="")
app.include_router(graphql_app, prefix="/graphql", tags=["GraphQL"])
