"""Pydantic models for manufacturers."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ManufacturerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)


class ManufacturerCreate(ManufacturerBase):
    pass


class Manufacturer(ManufacturerBase):
    id: int

    class Config:
        from_attributes = True
