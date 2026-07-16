from sqlalchemy import select,func
from sqlalchemy.orm import Session

from app.models.generated_content import GeneratedContent


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

def get_generated_content(
    db: Session,
    generated_id: int
)-> GeneratedContent | None:
    return db.get(
        GeneratedContent,
        generated_id
    )

def get_job_generated_contents(
    db: Session,
    job_id: int
)-> list[GeneratedContent]:

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

    return list(db.scalars(
        statement
    ).all()
    )

def get_latest_version(
    db: Session,
    job_id: int,
    platform: str
) -> int:
    latest = db.scalar(
        select(func.max(GeneratedContent.version))
        .where(
            GeneratedContent.job_id == job_id,
            GeneratedContent.platform == platform
        )
    )

    return latest or 0

def create_new_version(
    db: Session,
    job_id: int,
    platform: str,
    content: str
) -> GeneratedContent:
    version = (
        get_latest_version(
            db,
            job_id,
            platform
        ) + 1
    )

    generated = GeneratedContent(
        job_id=job_id,
        platform=platform,
        content=content,
        version=version
    )

    db.add(generated)

    db.commit()

    db.refresh(generated)

    return generated

def get_platform_versions(
    db: Session,
    job_id: int,
    platform: str
) -> list[GeneratedContent]:

    statement = (
        select(GeneratedContent)
        .where(
            GeneratedContent.job_id == job_id,
            GeneratedContent.platform == platform
        )
        .order_by(
            GeneratedContent.version.desc()
        )
    )

    return list(db.scalars(statement).all()
    )
