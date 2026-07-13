from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.db.base_class import Base


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    service: Mapped[str] = mapped_column(String, index=True, nullable=False)
    severity: Mapped[str] = mapped_column(String, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
