from database_service.abcs.database_service_abc import DatabaseServiceABC
from database_service.service import DatabaseService
from database_service.models import QueryModel
from .schema import URLShortener
import hashlib
import base64
import random

class URLShortenerService:
    def __init__(self, database: DatabaseServiceABC | None = None):
        self.database = database or DatabaseService(URLShortener)

    async def create_one(self, long_url: str):
        """Shortens a long URL and returns the short URL."""
        if (await self.get_all(QueryModel(filter={"long_url": long_url}))) > 0: raise ValueError("URL already shortened")
        salt = random.randint()
        short_url = await self._create_short_url(long_url, salt)
        while await self._short_url_exist(short_url):
            short_url = await self._create_short_url(long_url, salt + 1)
            salt += random.randint()
        
        return await self.database.create_one(short_url)

    async def get_one(self, short_url: str):
        """Retrieves the long URL from a short URL."""
        query = QueryModel(filter={"short_url": short_url}, limit=1)
        result = await self.database.get_all(query)
        if not result:
            raise ValueError("Short URL not found")
        return result[0].long_url

    async def get_all(self, query: QueryModel):
        """Returns all shortened URLs, optionally filtered by a query."""
        return await self.database.get_all(query)
    
    async def _get_short_url(self, long_url: str):
        """Gets a short URL back from the original long URL."""
        long_url = await self.database.get_one(long_url)
        return long_url
    
    async def _short_url_exist(self, short_url: str):
        """Checks if a short URL already exists in the database."""
        query = QueryModel(filter={"short_url": short_url}, limit=1)
        return len(await self.database.get_all(query)) > 0
    
    async def _create_short_url(self, long_url: str, salt = 0):
        """Asynchronously shortens a long URL and returns the short URL."""
        hash_object = hashlib.sha256(long_url.encode() + str(salt).encode())
        short_hash = hash_object.hexdigest()[:8]  # Take first 8 characters of the hash
        short_url = base64.b64encode(short_hash.encode()).decode('utf-8')
        return short_url