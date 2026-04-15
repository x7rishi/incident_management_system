from enum import StrEnum
import uuid 
from sqlalchemy import String, Text, ForeignKey, Enum 
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base, TimestampMixin
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.user import User

class IncidentStatus(StrEnum): 
    OPEN = 'open'
    INVESTIGATING = 'investigating'
    RESOLVED = 'resolved'
    CLOSED = 'closed'


class IncidentPriority(StrEnum): 
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'


class Incident(Base, TimestampMixin): 
    __tablename__ = 'incidents'
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[IncidentStatus] = mapped_column(
        Enum(IncidentStatus), 
        default=IncidentStatus.OPEN, 
        nullable=False
    )
    priority: Mapped[IncidentPriority] = mapped_column(
        Enum(IncidentPriority), 
        default=IncidentPriority.MEDIUM, 
        nullable=False
    )
    reporter_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False
    )
    assignee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), 
        nullable=True
    )
    reporter: Mapped["User"] = relationship(
        "User",
        foreign_keys=[reporter_id], 
        back_populates='reported_incidents'
    )
    assignee: Mapped["User"] = relationship(
        "User", 
        foreign_keys=[assignee_id],
        back_populates='assigned_tasks'
    )