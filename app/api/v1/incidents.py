from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks,Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from typing import Annotated

from app.db.session import get_db
from app.schemas.incident import IncidentCreate, IncidentRead
from app.services.incident import incident_service, search_service
from app.api.deps import get_current_user
from app.models.user import User
from app.models.incident import Incident

router = APIRouter()


@router.post("/", response_model=IncidentRead, status_code=status.HTTP_201_CREATED)
async def create_incident(
    incident_in: Annotated[IncidentCreate, Body()],
    db: Annotated[AsyncSession, Depends(get_db)],
    background_tasks: BackgroundTasks,
    current_user: Annotated[User, Depends(get_current_user)]
):
    mock_user_id = uuid.uuid4()
    return await incident_service.create_new_incident(
        db,
        incident_in=incident_in,
        reporter_id=current_user.id,
        background_tasks=background_tasks,
    )

from sqlalchemy import select
# ... other imports

@router.get("/", response_model=list[IncidentRead])
async def list_incidents(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = 100,
    offset: int = 0
):
    """
    Retrieve all incidents. 
    A senior dev adds limit/offset for pagination immediately.
    """
    query = select(Incident).offset(offset).limit(limit)
    result = await db.execute(query)
    incidents = result.scalars().all()
    return incidents

@router.get('/search',response_model=list[IncidentRead])
async def search_incidents(
    q: Annotated[str, Query(min_length = 3, description='Search query string')], 
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    search_results = await search_service.search_incidents(q)
    return search_results


# app/api/v1/incidents.py
from uuid import UUID

@router.patch("/{incident_id}", response_model=IncidentRead)
async def update_incident(
    incident_id: UUID,
    incident_in: dict, # For simplicity, we'll use a dict, but a Schema is better
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(Incident).where(Incident.id == incident_id)
    result = await db.execute(query)
    db_incident = result.scalar_one_or_none()
    
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    # Update fields
    for key, value in incident_in.items():
        setattr(db_incident, key, value)

    await db.commit()
    await db.refresh(db_incident)
    return db_incident