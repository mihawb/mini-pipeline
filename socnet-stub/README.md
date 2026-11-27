# Social Network mock-up

`socnet-stub` is a small social-network event producer used to populate the
project database with realistic test data. It continuously generates random
records and inserts them into PostgreSQL at a configurable rate.

## Structure

- `src/socnet_stub/main.py` - minimal Uvicorn entry point exposing `app`.
- `src/socnet_stub/app.py` - FastAPI application assembly.
- `src/socnet_stub/config.py` - environment loading and database URL setup.
- `src/socnet_stub/database.py` - SQLAlchemy engine setup.
- `src/socnet_stub/event_service.py` - background event-generation lifecycle
  and rate control.
- `src/socnet_stub/routes.py` - HTTP endpoints and template rendering.
- `src/socnet_stub/entities.py` - SQLAlchemy models for users, posts, follows,
  ratings, and comments.
- `src/socnet_stub/generation.py` - random entity generators, weighted
  dispatch, and database insert operations with constraint handling.
- `templates/index.html` - browser-based control console.

## Technology and features

- **Backend:** Python 3.15+, FastAPI, Uvicorn, SQLAlchemy, and psycopg.
- **Database:** PostgreSQL container, configured through `.env` file.
- **Frontend:** server-rendered Jinja2 HTML with HTMX for asynchronous updates.
- Generates random `User`, `Post`, `Follow`, `Rating`, and `Comment` entities
  adhering to the database schema.
- Selects existing user and post IDs from PostgreSQL when generating dependent
  entities.
- Skips posts, follows, ratings, and comments when the required users or posts do
  not exist.
- Selects one of five generators using configurable weights. The current
  equal-weight configuration gives each generator a 20% chance of selection.
- Handles database constraint violations during insertion without stopping the
  background event loop.
- Runs generation in the background while the service is alive.
- Provides a console slider to change the generation rate from 0 to 100
  events per minute without reloading the page; setting it to 0 pauses
  generation.

## Running

Run the FastAPI service from this directory with:

```bash
uv run uvicorn socnet_stub.main:app --host 0.0.0.0 --port 8000 --reload
```
