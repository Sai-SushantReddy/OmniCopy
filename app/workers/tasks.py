import time

from datetime import datetime

from app.db.session import SessionLocal

from app.models.job import (
    TransformationJob,
    JobStatus
)

from app.workers.celery_app import celery_app


@celery_app.task(
    name="process_transformation_job"
)
def process_transformation_job(
    job_id: int
):

    db = SessionLocal()

    try:

        job = db.get(
            TransformationJob,
            job_id
        )

        if job is None:
            return

        job.status = JobStatus.PROCESSING
        job.started_at = datetime.utcnow()

        db.commit()

        # Simulate slow AI processing
        time.sleep(10)

        job.status = JobStatus.COMPLETED
        job.completed_at = datetime.utcnow()

        db.commit()

    except Exception as exc:

        db.rollback()

        job = db.get(
            TransformationJob,
            job_id
        )

        if job is not None:

            job.status = JobStatus.FAILED
            job.error_message = str(exc)

            db.commit()

        raise

    finally:

        db.close()