from abc import ABCMeta
from typing import Generic, TypeVar, get_type_hints

from sqlalchemy.inspection import inspect

from src.core.databases.models.db_context import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseGraphSchema(Generic[ModelType], metaclass=ABCMeta):
    @classmethod
    def from_model(cls, data: ModelType):
        cls_field = get_type_hints(cls).keys()
        model_attrs = {
            c.key: getattr(data, c.key)
            for c in inspect(data).mapper.column_attrs
            if c.key in cls_field
        }

        return cls(**model_attrs)
