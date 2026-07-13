from sqlalchemy import Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from typing import Optional
from app.db.base_class import Base


class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    incident_id: Mapped[Optional[str]] = mapped_column(
        String, 
        ForeignKey("incidents.id"), 
        index=True, 
        nullable=True
    )
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    log_level: Mapped[str] = mapped_column(String, index=True, nullable=False)
    service: Mapped[str] = mapped_column(String, index=True, nullable=False)
    message: Mapped[str] = mapped_column(String, nullable=False)
    extra: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
