# from fastapi import APIRouter, Request, Depends, HTTPException, status, Form, Cookie
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.templating import Jinja2Templates
# from sqlalchemy.ext.asyncio import AsyncSession
# from datetime import datetime, timedelta
# from typing import Optional
# from jose import JWTError, jwt

# from app.models import User
# from app.database import get_db
# from app.security import authenticate_user, create_access_token, SECRET_KEY, ALGORITHM

# router = APIRouter(tags=["Authentication"])

# # Templates
# login_templates = Jinja2Templates(directory="frontend")

# @router.get("/", response_class=HTMLResponse)
# async def login_page(request: Request):
#     return login_templates.TemplateResponse("login.html", {"request": request})




# @router.post("/login", response_class=HTMLResponse)
# async def login(
#     request: Request,
#     username: str = Form(...),
#     password: str = Form(...),
#     db: AsyncSession = Depends(get_db)
# ):
#     # Authenticate user
#     user = await authenticate_user(db, username, password)
#     if not user:
#         return login_templates.TemplateResponse(
#             "login.html",
#             {"request": request, "error": "Invalid credentials"}
#         )

#     # Create access token with username and role
#     access_token_expires = timedelta(minutes=30)
#     access_token = create_access_token(
#         data={"sub": user.username, "role": user.role},
#         expires_delta=access_token_expires
#     )

#     # Set token in cookie and redirect to appropriate dashboard
#     if user.role == "admin":
#         redirect_url = "/admin/dashboard"
#     else:
#         redirect_url = "/reception/dashboard"
    
#     response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
#     response.set_cookie(
#         key="access_token",
#         value=access_token,
#         httponly=True,
#         max_age=1800,
#         samesite="lax"
#     )
#     return response





# @router.get("/logout")
# async def logout():
#     response = RedirectResponse(url="/")
#     response.delete_cookie("access_token")
#     return response