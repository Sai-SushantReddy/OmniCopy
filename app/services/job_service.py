from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.job import (
    TransformationJob,
    JobStatus
)

from app.schemas.job import TransformationRequest

import json

from app.core.redis import redis_client

def create_job(
    db: Session,
    user_id: int,
    content_id: int,
    data: TransformationRequest
):

    job = TransformationJob(
        user_id=user_id,
        content_id=content_id,
        status=JobStatus.QUEUED,
        tone=data.tone,
        platforms=",".join(data.platforms)
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_user_job(
    db: Session,
    user_id: int,
    job_id: int
):

    statement = select(
        TransformationJob
    ).where(
        TransformationJob.id == job_id,
        TransformationJob.user_id == user_id
    )

    return db.scalar(statement)


def get_user_jobs(
    db: Session,
    user_id: int
):

    statement = (
        select(TransformationJob)
        .where(
            TransformationJob.user_id == user_id
        )
        .order_by(
            TransformationJob.created_at.desc()
        )
    )

    return db.scalars(
        statement
    ).all()