from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.db.base import Base


class GeneratedContent(Base):

    __tablename__ = "generated_contents"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey("transformation_jobs.id"),
        nullable=False,
        index=True
    )

    platform: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )