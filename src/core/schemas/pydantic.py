from typing import Any

from pydantic import BaseModel, ConfigDict, alias_generators


class BasePydanticSchema(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        alias_generator=alias_generators.to_camel,
        populate_by_name=True,
    )

    @classmethod
    def from_strawberry(cls, input_obj: Any):
        input_dict = {
            k: v for k, v in input_obj.__dict__.items() if not k.startswith("_")
        }

        return cls(**input_dict)
