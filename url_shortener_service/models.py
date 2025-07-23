from pydantic import BaseModel

class CreateURLShortenerModel(BaseModel):
    long_url: str