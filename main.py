
from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from url_shortener_service.router import router as url_shortener_router
from dotenv import load_dotenv
from common.utils import get_all_schema
from database_service.service import DatabaseService

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()
    for schema in get_all_schema():
        db_service = DatabaseService(schema)
        await db_service.connect()
        await db_service.create_metadata()
    yield

app = FastAPI(lifespan=lifespan)

routers: list[APIRouter] = [url_shortener_router]
for router in routers:
    app.include_router(router)