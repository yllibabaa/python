# Airplane Rater (FastAPI + Streamlit)

A small project for **rating airplanes online**, inspired by the structure of the VideoGame Rater app.

## Features

### Public
- Browse manufacturers and airplanes
- See an airplane's **average score** and **rating count**
- Read recent ratings / reviews
- Submit a rating (score 1–10) with an optional comment

### Admin (API key)
- Create / update / delete manufacturers
- Create / update / delete airplanes
- Delete ratings (basic moderation)

## Architecture (similar to the original)
- **FastAPI backend** with routers (`routers/`), pydantic models (`models/`), and SQLite (`database.py`)
- **Streamlit frontend** (`app.py`) that calls the API via HTTP
- **API-key protection** for admin endpoints (`auth/security.py`)

## Project structure

```
videogame_rater/
  app.py                 # Streamlit UI
  main.py                # FastAPI app
  database.py            # SQLite setup/helpers
  seed_demo_data.py      # Optional demo data (manufacturers & airplanes)
  requirements.txt
  .env.example
  auth/
    __init__.py
    security.py
  models/
    __init__.py
    manufacturer.py
    airplane.py
    rating.py
  routers/
    __init__.py
    api_key.py
    studios.py
    games.py
    ratings.py
```

## Setup

### 1) Create and activate a virtual environment

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Configure environment

Copy `.env.example` to `.env` and edit:

```bash
cp .env.example .env
```

- `API_KEYS` controls admin access (comma-separated supported)
- `BASE_URL` is used by Streamlit to call FastAPI (usually `http://127.0.0.1:8000/api`)

### 4) (Optional) seed demo data

```bash
python seed_demo_data.py
```

## Run

### Backend (FastAPI)

```bash
uvicorn main:app --reload
```

Open docs:
- Swagger UI: `http://127.0.0.1:8000/docs`

### Frontend (Streamlit)

In a second terminal:

```bash
streamlit run app.py
```

## API quick examples

### List airplanes

```bash
curl "http://127.0.0.1:8000/api/airplanes/"
```

### Add a manufacturer (admin)

```bash
curl -X POST "http://127.0.0.1:8000/api/manufacturers/" \
  -H "Content-Type: application/json" \
  -H "api-key: change-me" \
  -d '{"name": "Boeing"}'
```

### Rate an airplane (public)

```bash
curl -X POST "http://127.0.0.1:8000/api/ratings/" \
  -H "Content-Type: application/json" \
  -d '{"airplane_id": 1, "score": 9, "username": "alex", "comment": "Great plane."}'
```

## How this differs from the original project

- **Domain swap:** books/authors → games/studios
- **Better data modeling for ratings:** instead of storing `average_rating` on the item, this project stores individual ratings in a dedicated table and computes averages (no stale aggregates)
- **Adds moderation tools:** admin can delete ratings
- **Adds leaderboard + rating histogram:** simple analytics in both API and Streamlit

