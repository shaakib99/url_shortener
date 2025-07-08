from database_service.abcs.database_abc import DatabaseABC
from .abcs.database_service_abc import DatabaseServiceABC
from typing import TypeVar
from sqlalchemy.orm import DeclarativeBase
from database_service.mysql_service.service import MySQLServiceSingleton

T = TypeVar('T', bound=DeclarativeBase)

class DatabaseService(DatabaseServiceABC):
    def __init__(self, schema, database: DatabaseABC | None = None):
        self.schema = schema
        self.database = database or MySQLServiceSingleton()
    
    async def connect(self) -> None:
        await self.database.connect()
    
    async def disconnect(self) -> None:
        await self.database.disconnect()
    
    async def create_one(self, data):
        return await self.database.create_one(data, self.schema)
    
    async def update_one(self, id: str, data):
        return await self.database.update_one(id, data, self.schema)
    
    async def get_one(self, id: str):
        return await self.database.get_one(id, self.schema)
    
    async def get_all(self, query) -> list:
        return await self.database.get_all(query, self.schema)

    async def delete_one(self, id: str) -> None:
        return await self.database.delete_one(id, self.schema)
    
    async def create_metadata(self):
        await self.database.create_metadata(self.schema)
