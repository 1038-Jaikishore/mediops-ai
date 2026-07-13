from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.db.base_class import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    incident_id: Mapped[str] = mapped_column(String, ForeignKey("incidents.id"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
