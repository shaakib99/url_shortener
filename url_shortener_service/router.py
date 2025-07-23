from fastapi import APIRouter
from url_shortener_service.service import URLShortenerService
from .models import CreateURLShortenerModel

router = APIRouter(prefix="/url_shortener")

service = URLShortenerService()

@router.post("/shorten")
async def shorten_url(data: CreateURLShortenerModel):
    """Endpoint to shorten a long URL."""
    return await service.create_one(data)

@router.get("/{short_url}")
async def get_long_url(short_url: str):
    return await service.get_one(short_url)