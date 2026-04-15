from elasticsearch import AsyncElasticsearch
from app.core.config import settings


class SearchService:
    def __init__(self):
        self.client = AsyncElasticsearch("http://localhost:9200")

    async def index_incident(self, incident):
        await self.client.index(
            index="incidents",
            id=str(incident.id),
            document={
                "id": str(incident.id),
                "title": incident.title,
                "description": incident.description,
                "status": incident.status,
                "priority": incident.priority,
                "reporter_id": str(incident.reporter_id),
                "created_at": incident.created_at.isoformat(),
                "updated_at": incident.updated_at.isoformat(),
            },
        )

    async def search_incidents(self, query: str):
        response = await self.client.search(
            index="incidents",
            query={
                "multi_match": {
                    "query": query,
                    "fields": ["title^3", "description"],
                    "fuzziness": "AUTO",
                }
            },
        )

        results = []
        for hit in response["hits"]['hits']:
            source = hit["_source"]
            if "id" not in source: 
                source["id"] = hit['_id']

            results.append(source)
        return results 


search_service = SearchService()
