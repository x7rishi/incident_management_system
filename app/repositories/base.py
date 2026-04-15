from typing import Generic, TypeVar, Type, Any 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.base import Base 

ModelType = TypeVar("ModelType", bound= Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model 

    async def get(self,db:AsyncSession,id:Any) ->ModelType | None:
        query = select(self.model).where(self.model.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def create(self,db: AsyncSession, *,obj_in:Any) -> ModelType:
        if isinstance(obj_in, dict): 
            obj_data = obj_in
        else: 
            obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj