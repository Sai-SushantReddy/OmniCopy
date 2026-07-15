from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict
)


class GeneratedContentResponse(BaseModel):

    id: int
    job_id: int
    platform: str
    content: str
    version: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )