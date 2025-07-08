
from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

routers: list[APIRouter] = []
for router in routers:
    app.include_router(router)