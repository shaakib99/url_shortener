from abc import ABC, abstractmethod
from sqlalchemy.orm import DeclarativeBase
from typing import TypeVar, Type, Generic
from pydantic import BaseModel
from database_service.abcs.database_abc import DatabaseABC

S = TypeVar('S', bound=DeclarativeBase)
T = TypeVar('T', bound=BaseModel)

class DatabaseServiceABC(Generic[S, T], ABC):
    def __init__(self, schema: Type[S]):
        pass

    @abstractmethod
    async def connect(self) -> None:
        """Establish a connection to the database."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close the connection to the database."""
        pass

    @abstractmethod
    async def create_one(self, data: T) -> S:
        """Create a single record in the database."""
        pass

    @abstractmethod
    async def get_one(self, id: str) -> S:
        """Read a single record from the database by its ID."""
        pass

    @abstractmethod
    async def get_all(self, query: T) -> list[S]:
        """Read all records from the database."""
        pass

    @abstractmethod
    async def update_one(self, id: str, data: T) -> S:
        """Update a single record in the database."""
        pass

    @abstractmethod
    async def delete_one(self, id: str) -> None:
        """Delete a single record from the database."""
        pass

    @abstractmethod
    async def create_metadata(self) -> None:
        """Create metadata for the database schema."""
        pass