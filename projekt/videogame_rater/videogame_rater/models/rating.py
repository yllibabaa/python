"""Pydantic models for ratings/reviews."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RatingCreate(BaseModel):
    game_id: int = Field(..., ge=1)
    score: int = Field(..., ge=1, le=10)
    username: Optional[str] = Field(default=None, max_length=60)
    comment: Optional[str] = Field(default=None, max_length=2000)


class Rating(BaseModel):
    id: int
    game_id: int
    score: int
    username: Optional[str] = None
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
