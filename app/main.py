from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db
from app.core.config import settings
from app.api.v1 import users, incidents, auth
from app.models import User, Incident
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)


app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(incidents.router, prefix=f"{settings.API_V1_STR}/incidents", tags=["Incidents"])

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health", tags=["Health"])
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Endpoint to verify the API is up and the Database connection is functional.
    """
    try:
        # Perform a simple query to check DB connectivity
        await db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "project": settings.PROJECT_NAME,
        }
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}


@app.get("/")
async def root():
    return {"message": "Welcome to the Enterprise Incident Management System"}
