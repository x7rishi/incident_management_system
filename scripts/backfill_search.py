import asyncio
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.incident import Incident
from app.services.search import search_service

async def backfill():
    print("Starting Elasticsearch backfill...")
    async with AsyncSessionLocal() as db:
        # Fetch all incidents
        result = await db.execute(select(Incident))
        incidents = result.scalars().all()
        
        for incident in incidents:
            print(f"Indexing incident: {incident.title}")
            await search_service.index_incident(incident)
            
    print(f"Successfully indexed {len(incidents)} incidents.")

if __name__ == "__main__":
    asyncio.run(backfill())