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

from app.schemas.generated_content import (
    GeneratedContentResponse
)

from app.services.job_service import (
    get_user_job
)

from app.services.generated_content_service import (
    get_job_generated_contents
)


router = APIRouter(
    prefix="/jobs",
    tags=["Generated Content"]
)


@router.get(
    "/{job_id}/outputs",
    response_model=list[GeneratedContentResponse]
)
def get_job_outputs(
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

    return get_job_generated_contents(
        db,
        job.id
    )