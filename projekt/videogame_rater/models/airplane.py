"""Pydantic models for airplanes."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class AirplaneCreate(BaseModel):
    model: str = Field(..., min_length=1, max_length=250)
    manufacturer_id: int = Field(..., ge=1)
    manufacture_year: Optional[int] = Field(default=None, ge=1903, le=2100)
    capacity: Optional[int] = Field(default=None, ge=1)
    types: List[str] = Field(default_factory=list)
    image_url: Optional[HttpUrl] = None


class Airplane(BaseModel):
    id: int
    model: str
    manufacturer_id: int
    manufacture_year: Optional[int] = None
    capacity: Optional[int] = None
    types: List[str] = Field(default_factory=list)
    image_url: Optional[HttpUrl] = None
    average_score: float = 0.0
    ratings_count: int = 0

    class Config:
        from_attributes = True
