from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

from app.models.job import JobStatus


class TransformationRequest(BaseModel):

    platforms: list[str] = Field(
        min_length=1
    )

    tone: str = Field(
        min_length=1,
        max_length=50
    )


class JobResponse(BaseModel):

    id: int
    user_id: int
    content_id: int
    status: JobStatus
    tone: str
    platforms: str

    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None
    error_message: str | None

    model_config = ConfigDict(
        from_attributes=True
    )