from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.database import Base, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # create_all создаёт таблицы, которых ещё нет; существующие не трогает
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="My project", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/items", response_model=schemas.ItemOut, status_code=201)
async def create_item(data: schemas.ItemCreate, db: AsyncSession = Depends(get_db)):
    item = models.Item(**data.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@app.get("/api/items", response_model=list[schemas.ItemOut])
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Item))
    return result.scalars().all()


@app.get("/api/items/{item_id}", response_model=schemas.ItemOut)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.get(models.Item, item_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return result


@app.delete("/api/items/{item_id}", status_code=204)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.get(models.Item, item_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await db.delete(result)
    await db.commit()
