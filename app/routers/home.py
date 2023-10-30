from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
router = APIRouter(tags=["home"])
@router.get("/", description="返回到文档主页")
async def home() -> RedirectResponse:
    return RedirectResponse("/docs")
