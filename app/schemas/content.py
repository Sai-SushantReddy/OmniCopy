from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class ContentCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=255
    )

    content: str = Field(
        min_length=1
    )

    content_type: str = Field(
        min_length=1,
        max_length=50
    )


class ContentUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=255
    )

    content: str | None = Field(
        default=None,
        min_length=1
    )

    content_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )


class ContentResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    content_type: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )