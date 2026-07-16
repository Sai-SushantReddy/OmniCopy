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


from app.models.generated_content import GeneratedContent
from app.models.job import TransformationJob
from app.models.content import Content

from app.schemas.generated_content import (
    GeneratedContentResponse
)

from app.services.job_service import (
    get_user_job
)

from app.services.generated_content_service import (
    get_job_generated_contents
)


from app.services.llm import generate_platform_content

from app.services.generated_content_service import (
    get_job_generated_contents,
    create_new_version,
    get_generated_content,
    get_platform_versions
)

router = APIRouter(
    prefix="/jobs",
    tags=["Generated Content"]
)

regenerated_router = APIRouter(
    prefix="/generated",
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

@regenerated_router.post(
    "/{generated_id}/regenerate",
    response_model=GeneratedContentResponse,
    status_code=status.HTTP_201_CREATED
)
def regenerate_content(
    generated_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    generated = get_generated_content(
        db,
        generated_id
    )

    if generated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generated content not found"
        )
    job = db.get(
        TransformationJob,
        generated.job_id
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    content = db.get(
        Content,
        job.content_id
    )

    if content is None:
        raise HTTPException(
            status_code=404,
            detail="Source content not found"
        )
    
    new_text = generate_platform_content(
        source_title = content.title,
        source_content = content.content,
        platform = generated.platform,
        tone=job.tone
    )

    new_version = create_new_version(
        db=db,
        job_id = job.id,
        platform=generated.platform,
        content=new_text
    )

    return new_version

@regenerated_router.get(
    "/{generated_id}/versions",
    response_model=list[GeneratedContentResponse]
)
def get_generated_versions(
    generated_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    generated = get_generated_content(
        db,
        generated_id
    )

    if generated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Generated content not found"
        )
    
    job = db.get(
        TransformationJob,
        generated.job_id
    )

    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden"
        )
    
    return get_platform_versions(
        db,
        job.id,
        generated.platform
    )
