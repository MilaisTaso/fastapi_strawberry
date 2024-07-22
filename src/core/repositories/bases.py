from abc import ABCMeta
from datetime import datetime
from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import BinaryExpression, delete, select, update
from sqlalchemy.exc import StatementError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.inspection import inspect
from sqlalchemy.orm.properties import ColumnProperty

from src.core.databases.models.db_context import DBContext
from src.core.schemas.pydantic import BasePydanticSchema

ModelType = TypeVar("ModelType", bound=DBContext)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BasePydanticSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BasePydanticSchema)


class DatabaseRepository(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType], metaclass=ABCMeta
):
    execute_columns = ["created_at", "updated_at", "deleted_at"]

    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    def _filtered_select_columns(self):
        mapper = inspect(subject=self.model, raiseerr=False)

        select_columns = [
            attr
            for attr in mapper.attrs
            if isinstance(attr, ColumnProperty) and attr not in self.execute_columns
        ]

        return select_columns

    async def create(
        self, data: CreateSchemaType, execute_none: bool = True
    ) -> ModelType:
        data_dict = data.model_dump(exclude_none=execute_none)
        context = self.model(**data_dict)

        self.session.add(context)
        await self.session.flush()
        await self.session.refresh(context)

        return context

    async def update(
        self, context: ModelType, data: UpdateSchemaType, execute_none: bool = True
    ) -> ModelType:
        data_dict = data.model_dump(exclude_none=execute_none)
        query = await self.session.execute(
            update(self.model).where(self.model.id == context.id), [data_dict]
        )
        if query.rowcount == 0:
            raise StatementError(
                message="Data was not updated",
                params=data_dict,
                orig=None,
                statement=str(query),
            )

        await self.session.flush()
        await self.session.refresh(context)

        return context

    async def get_context_by_id(self, id: UUID) -> ModelType | None:
        # get()は主キーに基づいたインスタンスを返す
        return await self.session.get(self.model, id)

    async def delete(self, context: ModelType) -> None:
        if hasattr(context, "deleted_at"):
            stmt = (
                update(self.model)
                .values(deleted_at=datetime.now())
                .where(self.model.id == context.id)
            )
            query = await self.session.execute(stmt)
        else:
            stmt = delete(self.model).where(self.model.id == context.id)
            query = await self.session.execute(stmt)

        if query.rowcount == 0:
            raise StatementError(
                message="Data failed logical deletion.",
                params=None,
                orig=None,
                statement=str(query),
            )

        return None

    async def get_context(self, *expressions: BinaryExpression) -> ModelType | None:
        select_columns = self._filtered_select_columns()
        if not expressions:
            return None

        stmt = select(self.model, *select_columns).where(*expressions)
        return await self.session.scalar(stmt)

    async def get_list_context(
        self,
        *expressions: BinaryExpression,
    ) -> list[ModelType]:
        select_columns = self._filtered_select_columns()
        query = select(self.model, *select_columns)

        if expressions:
            query = query.where(*expressions)

        return list(await self.session.scalars(query))
