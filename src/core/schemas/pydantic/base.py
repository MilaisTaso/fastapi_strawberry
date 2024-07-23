from pydantic import BaseModel, ConfigDict, alias_generators


class BasePydanticSchema(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        alias_generator=alias_generators.to_camel,
        populate_by_name=True,
    )
