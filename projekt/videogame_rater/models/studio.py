"""Pydantic models for studios."""

from __future__ import annotations

from pydantic import BaseModel, Field


class StudioBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)


class StudioCreate(StudioBase):
    pass


class Studio(StudioBase):
    id: int

    class Config:
        from_attributes = True
