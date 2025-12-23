"""API-key validation endpoint for the Streamlit frontend."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from auth.security import get_api_key

router = APIRouter()


@router.get("/", response_model=dict)
def validate_key(_: str = Depends(get_api_key)) -> dict:
    return {"detail": "OK"}
