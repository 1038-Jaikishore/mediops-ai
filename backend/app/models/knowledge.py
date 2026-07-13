from sqlalchemy import Integer, String, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.db.base_class import Base


class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    tags: Mapped[dict] = mapped_column(JSON, default=list, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
