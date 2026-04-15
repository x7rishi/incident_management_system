from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.incident import incident_repo
from app.schemas.incident import IncidentCreate
from app.models.incident import Incident
from fastapi import BackgroundTasks
from app.services.search import search_service


class IncidentService:
    async def create_new_incident(
        self,
        db: AsyncSession,
        *,
        incident_in: IncidentCreate,
        reporter_id,
        background_tasks: BackgroundTasks 
    ) -> Incident:
        incident_data = incident_in.model_dump()
        incident_data["reporter_id"] = reporter_id

        db_obj = await incident_repo.create(db, obj_in=incident_data)
        background_tasks.add_task(search_service.index_incident, db_obj)
        return db_obj


incident_service = IncidentService()
