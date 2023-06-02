from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from service_backend.helpers.utils import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):    
    context = {
        "request": request,
        "title": "Welcome Socket.io",               
    }
    return templates.TemplateResponse("index.html", context)