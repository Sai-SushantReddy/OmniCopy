from datetime import datetime

from app.core.logger import logger
from app.db.session import SessionLocal

from app.models.content import Content

from app.models.job import (
    TransformationJob,
    JobStatus
)

from app.services.generated_content_service import (
    create_generated_content
)

from app.services.llm import (
    generate_platform_content
)

from app.workers.celery_app import celery_app


@celery_app.task(
    bind=True,
    name="process_transformation_job",
    max_retries=3
)
def process_transformation_job(
    self,
    job_id: int
):

    db = SessionLocal()

    try:

        job = db.get(
            TransformationJob,
            job_id
        )

        if job is None:
            logger.warning("Transformation job %s not found",job_id)
            return

        content = db.get(
            Content,
            job.content_id
        )

        if content is None:
            raise ValueError(
                "Source content not found"
            )

        logger.info(
            "Job %s processing",
            job.id
        )
        job.status = JobStatus.PROCESSING
        job.started_at = datetime.utcnow()
        job.error_message = None

        db.commit()

        platforms = [
            platform.strip()
            for platform in job.platforms.split(",")
        ]

        for platform in platforms:

            logger.info(
                "Generating %s content for job %s",
                platform,
                job.id
            )

            generated_text = (
                generate_platform_content(
                    source_title=content.title,
                    source_content=content.content,
                    platform=platform,
                    tone=job.tone
                )
            )

            create_generated_content(
                db=db,
                job_id=job.id,
                platform=platform,
                content=generated_text
            )

        job.status = JobStatus.COMPLETED
        job.completed_at = datetime.utcnow()

        db.commit()

        logger.info("Job %s completed successfully",job.id)

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

        logger.exception(
            "Job %s failed",
            job_id
        )

        raise

    finally:

        db.close()