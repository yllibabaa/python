from pydantic import BaseModel


class MovieCreate(BaseModel):
    tittle: str
    director: str


class Movie(MovieCreate):
    id: int
