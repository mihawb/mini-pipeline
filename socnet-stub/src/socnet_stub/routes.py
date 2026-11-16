from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates

from .event_service import EventGenerator

templates = Jinja2Templates(directory=Path(__file__).resolve().parents[2] / "templates")


def create_router(event_generator: EventGenerator) -> APIRouter:
    router = APIRouter()

    @router.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        return templates.TemplateResponse(request=request, name="index.html")

    @router.post("/update-epm")
    async def update_epm(requested_epm: int = Form(..., alias="epm")):
        current_epm = event_generator.update_rate(requested_epm)
        return Response(content=str(current_epm), media_type="text/plain")

    return router
