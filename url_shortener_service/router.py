from fastapi import APIRouter
from url_shortener_service.service import URLShortenerService

router = APIRouter(prefix="/url_shortener")

service = URLShortenerService()

@router.post("/shorten")
async def shorten_url(long_url: str):
    """Endpoint to shorten a long URL."""
    return await service.create_one(long_url)

@router.get("/{short_url}")
async def get_long_url(short_url: str):
    return await service.get_one(short_url)