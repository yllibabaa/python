"""Pydantic models for games."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class GameCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=250)
    studio_id: int = Field(..., ge=1)
    release_year: Optional[int] = Field(default=None, ge=1970, le=2100)
    platforms: List[str] = Field(default_factory=list)
    genres: List[str] = Field(default_factory=list)
    cover_url: Optional[HttpUrl] = None


class Game(BaseModel):
    id: int
    title: str
    studio_id: int
    release_year: Optional[int] = None
    platforms: List[str] = Field(default_factory=list)
    genres: List[str] = Field(default_factory=list)
    cover_url: Optional[HttpUrl] = None
    average_score: float = 0.0
    ratings_count: int = 0

    class Config:
        from_attributes = True
