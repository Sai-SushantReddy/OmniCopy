from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.generated_content import (
    GeneratedContent
)


def create_generated_content(
    db: Session,
    job_id: int,
    platform: str,
    content: str,
    version: int = 1
):

    generated_content = GeneratedContent(
        job_id=job_id,
        platform=platform,
        content=content,
        version=version
    )

    db.add(generated_content)

    return generated_content


def get_job_generated_contents(
    db: Session,
    job_id: int
):

    statement = (
        select(GeneratedContent)
        .where(
            GeneratedContent.job_id == job_id
        )
        .order_by(
            GeneratedContent.platform,
            GeneratedContent.version
        )
    )

    return db.scalars(
        statement
    ).all()