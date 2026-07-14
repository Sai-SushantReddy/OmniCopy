from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Response,
    status
)

from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User

from app.schemas.content import (
    ContentCreate,
    ContentUpdate,
    ContentResponse
)

from app.services.content_service import (
    create_content,
    get_user_contents,
    get_user_content,
    update_content,
    delete_content
)

from app.schemas.job import (
    TransformationRequest,
    JobResponse
)

from app.services.job_service import create_job

from app.workers.tasks import (
    process_transformation_job
)

router = APIRouter(
    prefix="/contents",
    tags=["Contents"]
)


@router.post(
    "",
    response_model=ContentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_content(
    data: ContentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return create_content(
        db,
        current_user.id,
        data
    )


@router.get(
    "",
    response_model=list[ContentResponse]
)
def list_contents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_user_contents(
        db,
        current_user.id
    )

@router.post(
    "/{content_id}/transform",
    response_model=JobResponse,
    status_code=status.HTTP_202_ACCEPTED
)
def transform_content(
    content_id: int,
    data: TransformationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    content = get_user_content(
        db,
        current_user.id,
        content_id
    )

    if content is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    job = create_job(
        db,
        current_user.id,
        content.id,
        data
    )

    process_transformation_job.delay(
        job.id
    )

    return job

@router.get(
    "/{content_id}",
    response_model=ContentResponse
)
def get_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    content = get_user_content(
        db,
        current_user.id,
        content_id
    )

    if content is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    return content


@router.patch(
    "/{content_id}",
    response_model=ContentResponse
)
def modify_content(
    content_id: int,
    data: ContentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    content = get_user_content(
        db,
        current_user.id,
        content_id
    )

    if content is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    return update_content(
        db,
        content,
        data
    )


@router.delete(
    "/{content_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_content(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    content = get_user_content(
        db,
        current_user.id,
        content_id
    )

    if content is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    delete_content(
        db,
        content
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )