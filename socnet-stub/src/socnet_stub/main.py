from fastapi import FastAPI

from .database import engine
from .event_service import EventGenerator
from .routes import create_router


def create_app() -> FastAPI:
    event_generator = EventGenerator(engine)
    app = FastAPI(lifespan=event_generator.lifespan)
    app.include_router(create_router(event_generator))
    return app


app = create_app()
