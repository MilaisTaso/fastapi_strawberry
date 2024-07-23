from abc import ABCMeta
from typing import Generic, get_type_hints

from sqlalchemy.inspection import inspect

from src.core.repositories.bases import ModelType


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
