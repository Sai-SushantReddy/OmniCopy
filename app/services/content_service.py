from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.content import Content
from app.schemas.content import (
    ContentCreate,
    ContentUpdate
)


def create_content(
    db: Session,
    user_id: int,
    data: ContentCreate
):

    content = Content(
        user_id=user_id,
        title=data.title,
        content=data.content,
        content_type=data.content_type
    )

    db.add(content)
    db.commit()
    db.refresh(content)

    return content


def get_user_contents(
    db: Session,
    user_id: int
):

    statement = (
        select(Content)
        .where(
            Content.user_id == user_id
        )
        .order_by(
            Content.created_at.desc()
        )
    )

    return db.scalars(
        statement
    ).all()


def get_user_content(
    db: Session,
    user_id: int,
    content_id: int
):

    statement = select(Content).where(
        Content.id == content_id,
        Content.user_id == user_id
    )

    return db.scalar(statement)


def update_content(
    db: Session,
    content: Content,
    data: ContentUpdate
):

    update_data = data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(
            content,
            field,
            value
        )

    db.commit()
    db.refresh(content)

    return content


def delete_content(
    db: Session,
    content: Content
):

    db.delete(content)
    db.commit()