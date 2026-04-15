import uuid
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.incident import Incident

class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    full_name: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    reported_incidents: Mapped[list["Incident"]] = relationship(
        "Incident",
        foreign_keys="Incident.reporter_id",
        back_populates="reporter"
    )
    assigned_tasks: Mapped[list["Incident"]] = relationship(
        "Incident",
        foreign_keys="[Incident.assignee_id]",
        back_populates="assignee"
    )
