from pydantic import BaseModel, ConfigDict, alias_generators


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        frozen=True,
        alias_generator=alias_generators.to_camel,
        populate_by_name=True,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
