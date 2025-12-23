"""FastAPI entrypoint for VideoGame Rater."""

from __future__ import annotations

from fastapi import FastAPI

from database import create_database
from routers import api_key, airplanes, ratings, manufacturers

app = FastAPI(
    title="Airplane Rater",
    description="An API for rating airplanes online (manufacturers, airplanes, and reviews).",
    version="1.0.0",
)
app.include_router(manufacturers.router, prefix="/api/manufacturers", tags=["Manufacturers"])
app.include_router(airplanes.router, prefix="/api/airplanes", tags=["Airplanes"])
app.include_router(ratings.router, prefix="/api/ratings", tags=["Ratings"])
app.include_router(api_key.router, prefix="/api/validate_key", tags=["Admin"])


@app.on_event("startup")
def on_startup() -> None:
    create_database()
