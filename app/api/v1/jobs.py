from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db

from app.models.user import User

from app.schemas.job import JobResponse

from app.services.job_service import (
    get_user_job,
    get_user_jobs
)


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.get(
    "",
    response_model=list[JobResponse]
)
def list_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_user_jobs(
        db,
        current_user.id
    )


@router.get(
    "/{job_id}",
    response_model=JobResponse
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    job = get_user_job(
        db,
        current_user.id,
        job_id
    )

    if job is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    return job