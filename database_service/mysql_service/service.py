from ..abcs.database_abc import DatabaseABC
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common.exceptions import NotFoundException
from pydantic import BaseModel
import os

class MySQLService(DatabaseABC):
    def __init__(self):
        self.url = os.getenv('MYSQL_URL', 'test')
        self.engine = create_engine(self.url)
        self.session = sessionmaker(bind=self.engine)()
    
    async def connect(self):
        """Establish a connection to the MySQL database."""
        self.engine.connect()

    async def disconnect(self):
        """Close the connection to the MySQL database."""
        self.engine.dispose()
    
    async def create_metadata(self, schema):
        schema.metadata.create_all(bind=self.engine)

    async def create_one(self, data, schema):
        """Create a single record in the MySQL database."""
        if isinstance(data, BaseModel):
            data_model = schema(**data.model_dump())
        elif isinstance(data, dict):
            data_model = schema(**data)
        else:
            data_model = data
        self.session.add(data_model)
        self.session.commit()
        self.session.flush()
        return data_model

    async def get_one(self, id: str, schema):
        """Read a single record from the MySQL database by its ID."""
        data = self.session.query(schema).filter(schema.id == id).first()
        if not data: raise NotFoundException('record not found')
        return data

    async def get_all(self, query, schema):
        """Read all records from the MySQL database."""
        cursor = self.session.query(schema)
        if query.sort_by:
            cursor = cursor.order_by(query.sort_by)
        if query.filter:
            for key, value in query.filter.items():
                cursor = cursor.filter(getattr(schema, key) == value)
        if query.fields:
            cursor = cursor.with_entities(*[getattr(schema, field) for field in query.fields])
        # cursor = cursor.limit(query.limit)
        # cursor = cursor.offset(query.skip)
        print(cursor)
        return cursor.all()

    async def update_one(self, id: str, data, schema):
        """Update a single record in the MySQL database."""
        record = await self.get_one(id, schema)
        for key, value in data.model_dump().items():
            setattr(record, key, value)
        self.session.commit()
        return record

    async def delete_one(self, id: str, schema):
        """Delete a single record from the MySQL database."""
        record = await self.get_one(id, schema)
        self.session.delete(record)
        self.session.commit()
    
    def get_db_url(self):
        return self.url

class MySQLServiceSingleton:
    _instance = None
    def __new__(cls) -> "DatabaseABC":
        if cls._instance is not None: return cls._instance
        cls._instance = MySQLService()
        return cls._instance
        