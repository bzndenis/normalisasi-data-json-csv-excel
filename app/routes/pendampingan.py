from fastapi import APIRouter, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from app.services.pendampingan_service import PendampinganService
import shutil
import os

router = APIRouter(
    prefix="/pendampingan",
    tags=["Pendampingan"]
)

templates = Jinja2Templates(directory="templates")
service = PendampinganService()

@router.get("/", response_class=HTMLResponse)
async def pendampingan_page(request: Request):
    """Pendampingan Management Page"""
    return templates.TemplateResponse(
        "pendampingan.html",
        {"request": request}
    )

@router.post("/import")
async def import_pendampingan(file: UploadFile = File(...)):
    """Import Pendampingan Data handle as SSE"""
    content = await file.read()
    
    return StreamingResponse(
        service.process_import(content),
        media_type="text/event-stream"
    )

from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
import os
from app.config import settings

# ... (rest of imports)

@router.get("/exports/{filename}")
async def download_export(filename: str):
    file_path = os.path.join(settings.EXPORT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    return {"error": "File not found"}

@router.post("/validate")
async def validate_pendampingan(
    file: UploadFile = File(...),
    fix: bool = Form(False),
    dry_run: bool = Form(False)
):
    """Validate Pendampingan Data"""
    content = await file.read()
    result = service.validate_data(content, fix=fix, dry_run=dry_run)
    return result
