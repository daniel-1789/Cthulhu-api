from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.database import engine, get_session
from app.schemas import AdventureCreate, AdventureRead, NPCCreate, NPCRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Dispose pooled connections on shutdown so uvicorn exits cleanly.
    await engine.dispose()


app = FastAPI(
    title="Cthulhu Adventures",
    description="Cthulhu adventures db interface: FastAPI + SQLAlchemy (async) + Alembic + Pydantic.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/adventures", response_model=list[AdventureRead])
async def list_adventures(
    name: str | None = None, session: AsyncSession = Depends(get_session)
):
    return await crud.list_adventures(session, name=name)


@app.get("/adventures/{adventure_id}", response_model=AdventureRead)
async def get_adventure(adventure_id: int, session: AsyncSession = Depends(get_session)):
    adventure = await crud.get_adventure(session, adventure_id)
    if adventure is None:
        raise HTTPException(status_code=404, detail=f"Adventure {adventure_id} not found")
    return adventure

@app.get("/adventure_names/{adventure_name}", response_model=AdventureRead)
async def get_adventure_by_name(adventure_name: str, session: AsyncSession = Depends(get_session)):
    adventure = await crud.get_adventure_by_name(session, adventure_name)
    if adventure is None:
        raise HTTPException(status_code=404, detail=f"Adventure {adventure_name} not found")
    return adventure

@app.post("/adventures", response_model=AdventureRead, status_code=201)
async def create_adventure(payload: AdventureCreate, session: AsyncSession = Depends(get_session)):
    return await crud.create_adventure(session, payload)


@app.get("/adventures/{adventure_id}/npcs", response_model=list[NPCRead])
async def list_npcs_in_adventure(
    adventure_id: int, session: AsyncSession = Depends(get_session)
):
    return await crud.list_npcs_in_adventure(session, adventure_id)


@app.get("/npcs", response_model=list[NPCRead])
async def list_npcs(
    name: str | None = None, session: AsyncSession = Depends(get_session)
):
    return await crud.list_npcs(session, name=name)


@app.get("/npcs/{npc_id}", response_model=NPCRead)
async def get_npc(npc_id: int, session: AsyncSession = Depends(get_session)):
    npc = await crud.get_npc(session, npc_id)
    if npc is None:
        raise HTTPException(status_code=404, detail=f"NPC {npc_id} not found")
    return npc


@app.get("/npc_names/{npc_name}", response_model=NPCRead)
async def get_npc_by_name(npc_name: str, session: AsyncSession = Depends(get_session)):
    npc = await crud.get_npc_by_name(session, npc_name)
    if npc is None:
        raise HTTPException(status_code=404, detail=f"NPC {npc_name} not found")
    return npc


@app.post("/npcs", response_model=NPCRead, status_code=201)
async def create_npc(payload: NPCCreate, session: AsyncSession = Depends(get_session)):
    return await crud.create_npc(session, payload)
