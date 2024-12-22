from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from server_utils import limiter
from process_query import process_query
from config import EXAMPLE_REPOS


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.jinja", 
        {
            "request": request,
            "examples": EXAMPLE_REPOS,
            "default_file_size": 243
        }
    )


@router.post("/", response_class=HTMLResponse)
@limiter.limit("10/minute") 
async def index_post(
    request: Request, 
    input_text: str = Form(...),
    max_file_size: int = Form(...),
    pattern_type: str = Form(...),
    pattern: str = Form(...)
):
    return await process_query(request, input_text, max_file_size, pattern_type, pattern, is_index=True)
    
    



