from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AdventureBrief(BaseModel):
    """Lightweight adventure reference for embedding in other responses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class AdventureCreate(BaseModel):
    """Payload for POST /adventures."""

    name: str = Field(..., max_length=255, examples=["The Dunwich Horror"])
    description: str | None = Field(None, max_length=1024)
    date_played: datetime | None = None

class AdventureRead(BaseModel):
    """Adventure as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    date_played: datetime | None
    created_at: datetime


class NPCCreate(BaseModel):
    """Payload for POST /npcs."""

    name: str = Field(..., max_length=255, examples=["Henry Armitage"])
    description: str | None = Field(None, max_length=1024)


class NPCRead(BaseModel):
    """NPC as returned by the API, with the adventures they appear in."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    adventures: list[AdventureBrief]
