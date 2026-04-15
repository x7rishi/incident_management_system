from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks,Query
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
    *,
    db: Annotated[AsyncSession, Depends(get_db)],
    incident_in: Annotated[IncidentCreate, Depends()],
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
