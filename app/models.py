from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


adventure_npcs = Table(
    "adventure_npcs",
    Base.metadata,
    Column("adventure_id", ForeignKey("adventures.id", ondelete="CASCADE"), primary_key=True),
    Column("npc_id", ForeignKey("npcs.id", ondelete="CASCADE"), primary_key=True),
)


class Adventure(Base):
    __tablename__ = "adventures"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(1024), default=None)
    date_played: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    npcs: Mapped[list["NPC"]] = relationship(
        secondary=adventure_npcs, back_populates="adventures"
    )


class NPC(Base):
    __tablename__ = "npcs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(1024), default=None)

    adventures: Mapped[list["Adventure"]] = relationship(
        secondary=adventure_npcs, back_populates="npcs"
    )
