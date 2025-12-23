"""Simple API key auth for admin endpoints.

The original project used a single API key in an `api-key` header.
This version keeps that UX but supports multiple keys.

Environment:
- API_KEYS: comma-separated keys, e.g. "key1,key2" (required for admin endpoints)
"""

from __future__ import annotations

import os
from typing import Set

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

load_dotenv()

API_KEY_NAME = "api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def _load_keys() -> Set[str]:
    raw = os.getenv("API_KEYS", "")
    return {k.strip() for k in raw.split(",") if k.strip()}


def get_api_key(api_key: str | None = Depends(api_key_header)) -> str:
    """Validate the provided API key.

    Used as a FastAPI dependency:
        def create_game(..., _: str = Depends(get_api_key))

    Raises:
        HTTPException: if the key is missing or invalid.
    """
    valid = _load_keys()
    if not valid:
        # Fail closed: if no admin keys are configured, admin endpoints are unavailable.
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Admin API keys are not configured (set API_KEYS).",
        )

    if api_key is None or api_key not in valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key.",
        )

    return api_key
