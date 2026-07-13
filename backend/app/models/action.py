from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.db.base_class import Base


class Action(Base):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    incident_id: Mapped[str] = mapped_column(String, ForeignKey("incidents.id"), index=True, nullable=False)
    action_type: Mapped[str] = mapped_column(String, nullable=False)
    command: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, index=True, nullable=False)
    log_output: Mapped[str] = mapped_column(String, default="", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
