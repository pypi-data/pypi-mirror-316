from pydantic import BaseModel


class DefaultValue[T](BaseModel):
    value: T
