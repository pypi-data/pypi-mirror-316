from pydantic import BaseModel, Field, ConfigDict

from . import DefaultValue


class ErrorDetails[T](BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    description: str
    default_value: DefaultValue[T] | None = Field(None, alias="defaultValue")
