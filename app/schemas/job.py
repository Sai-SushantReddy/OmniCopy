from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator
)

from app.models.job import JobStatus

from app.services.platform_service import (
    SUPPORTED_PLATFORMS
)


class TransformationRequest(BaseModel):

    platforms: list[str] = Field(
        min_length=1
    )

    tone: str = Field(
        min_length=1,
        max_length=50
    )

    @field_validator("platforms")
    @classmethod
    def validate_platforms(
        cls,
        platforms: list[str]
    ) -> list[str]:

        normalized_platforms = [
            platform.lower().strip()
            for platform in platforms
        ]

        invalid_platforms = (
            set(normalized_platforms)
            - SUPPORTED_PLATFORMS
        )

        if invalid_platforms:
            raise ValueError(
                "Unsupported platforms: "
                + ", ".join(invalid_platforms)
            )

        return list(
            dict.fromkeys(normalized_platforms)
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