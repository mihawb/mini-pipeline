import asyncio
import logging
from contextlib import suppress
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from .generation import insert_entity, random_generator_dispatch

logger = logging.getLogger("SocialNetworkStub")


class EventGenerator:
    def __init__(self, engine: Engine, events_per_minute: int = 0):
        self.engine = engine
        self.events_per_minute = events_per_minute
        self.rate_changed = asyncio.Event()

    async def run(self) -> None:
        while True:
            current_epm = self.events_per_minute

            if current_epm <= 0:
                await self.rate_changed.wait()
                self.rate_changed.clear()
                continue

            try:
                generator = random_generator_dispatch()
                entity = generator(self.engine)
                if entity is not None:
                    await asyncio.to_thread(insert_entity, self.engine, entity)
            except SQLAlchemyError:
                logger.exception("Could not insert generated event")

            try:
                await asyncio.wait_for(
                    self.rate_changed.wait(),
                    timeout=60 / current_epm,
                )
            except asyncio.TimeoutError:
                continue
            else:
                self.rate_changed.clear()

    def update_rate(self, requested_epm: int) -> int:
        self.events_per_minute = max(0, min(requested_epm, 1000))
        self.rate_changed.set()
        logger.info(
            "Event generation speed updated to %s events/min",
            self.events_per_minute,
        )
        return self.events_per_minute

    async def lifespan(self, _: FastAPI) -> AsyncGenerator[None]:
        task = asyncio.create_task(self.run())
        try:
            yield
        finally:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
