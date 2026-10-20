from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Message(BaseModel):
    # Fields are snake_case in Python and camelCase in JSON (createdAt).
    model_config = ConfigDict(
        from_attributes=True, alias_generator=to_camel, validate_by_name=True
    )

    id: int
    text: str
    created_at: datetime
