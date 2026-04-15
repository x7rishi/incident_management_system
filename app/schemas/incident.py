import uuid
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from app.models.incident import IncidentStatus, IncidentPriority

class IncidentBase(BaseModel):
    title: str = Field(...,min_length=5, max_length=255)
    description: str = Field(...,min_length=10)
    priority: IncidentPriority = IncidentPriority.MEDIUM


class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    title: str | None = None 
    description: str | None = None 
    status : IncidentStatus | None = None 
    priority: IncidentPriority | None = None 
    assignee_id: uuid.UUID | None = None 


class IncidentRead(IncidentBase):
    id: uuid.UUID
    status: IncidentStatus
    reporter_id: uuid.UUID
    assignee_id: uuid.UUID | None = None 
    created_at : datetime 
    updated_at: datetime 
    model_config = ConfigDict(from_attributes=True)
    