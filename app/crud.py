from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import NPC, Adventure
from app.schemas import AdventureCreate, NPCCreate


async def list_adventures(
    session: AsyncSession, name: str | None = None
) -> list[Adventure]:
    stmt = select(Adventure).order_by(Adventure.id)
    if name:
        stmt = stmt.where(Adventure.name.ilike(f"%{name}%"))
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_adventure(session: AsyncSession, adventure_id: int) -> Adventure | None:
    return await session.get(Adventure, adventure_id)

async def get_adventure_by_name(session: AsyncSession, adventure_name: str) -> Adventure | None:
    stmt = select(Adventure).where(Adventure.name == adventure_name)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def create_adventure(session: AsyncSession, data: AdventureCreate) -> Adventure:
    adventure = Adventure(**data.model_dump())
    session.add(adventure)
    await session.commit()
    await session.refresh(adventure)
    return adventure


async def list_npcs(session: AsyncSession, name: str | None = None) -> list[NPC]:
    stmt = (
        select(NPC)
        .options(selectinload(NPC.adventures))
        .order_by(NPC.id)
    )
    if name:
        stmt = stmt.where(NPC.name.ilike(f"%{name}%"))
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_npc(session: AsyncSession, npc_id: int) -> NPC | None:
    stmt = (
        select(NPC)
        .where(NPC.id == npc_id)
        .options(selectinload(NPC.adventures))
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_npc_by_name(session: AsyncSession, npc_name: str) -> NPC | None:
    stmt = (
        select(NPC)
        .where(NPC.name == npc_name)
        .options(selectinload(NPC.adventures))
    )
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def list_npcs_in_adventure(
    session: AsyncSession, adventure_id: int
) -> list[NPC]:
    stmt = (
        select(NPC)
        .where(NPC.adventures.any(Adventure.id == adventure_id))
        .options(selectinload(NPC.adventures))
        .order_by(NPC.id)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def create_npc(session: AsyncSession, data: NPCCreate) -> NPC:
    npc = NPC(**data.model_dump())
    session.add(npc)
    await session.commit()
    # Re-fetch with adventures eager-loaded so the response can render the brief list.
    return await get_npc(session, npc.id)  # type: ignore[return-value]
