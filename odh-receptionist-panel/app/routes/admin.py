# from fastapi import APIRouter, Request, Depends, HTTPException, status
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates

# router = APIRouter(tags=["Admin"])

# # Templates
# admin_templates = Jinja2Templates(directory="frontend/admin/templates")

# @router.get("/admin/dashboard", response_class=HTMLResponse)
# async def admin_dashboard(
#     request: Request
# ):
#     # Admin dashboard logic will be added later
#     return admin_templates.TemplateResponse(
#         "index.html",
#         {"request": request}
#     )