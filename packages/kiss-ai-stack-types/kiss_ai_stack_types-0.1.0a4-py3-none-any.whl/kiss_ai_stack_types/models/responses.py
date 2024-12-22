from typing import Any

from pydantic import BaseModel, Field


class GenericResponseBody(BaseModel):
    stack_id: str = Field('', description='Stack/session Id')
    result: Any = Field(None, description='Generated answer')
    extras: Any = Field(None, description='Other return values')
