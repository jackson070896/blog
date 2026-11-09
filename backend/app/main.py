from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.auth.models  # noqa: F401 — модели должны попасть в Base.metadata
import app.posts.models  # noqa: F401
from app.auth.router import router as auth_router
from app.posts.router import router as posts_router
from app.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # создаёт таблицы, которых ещё нет; существующие не трогает
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="FastAPI Blog", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(posts_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
