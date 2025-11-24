# from fastapi import APIRouter, Request, Depends, HTTPException, status, Form, Cookie, Query
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.templating import Jinja2Templates
# from sqlalchemy.ext.asyncio import AsyncSession
# from datetime import datetime, timedelta, date
# from typing import Optional, List
# from jose import JWTError, jwt
# from sqlalchemy import select, func

# from app.models import User, Visitor
# from app.database import get_db
# from app.security import SECRET_KEY, ALGORITHM
# from app import crud

# router = APIRouter(tags=["Reception"])

# # Templates
# reception_templates = Jinja2Templates(directory="frontend/reception/templates")

# # ---------------- HELPER FUNCTIONS ---------------- #
# async def get_current_user(
#     request: Request,
#     db: AsyncSession = Depends(get_db),
#     access_token: Optional[str] = Cookie(None)
# ):
#     """Get current user from token in cookie or authorization header"""
#     token = access_token
#     if not token:
#         auth_header = request.headers.get("Authorization")
#         if auth_header and auth_header.startswith("Bearer "):
#             token = auth_header[7:]

#     if not token:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Not authenticated",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         role: str = payload.get("role")
#         if not username or not role:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid token payload",
#             )
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#         )

#     # Fetch user from DB
#     result = await db.execute(select(User).where(User.username == username))
#     user = result.scalars().first()
#     if not user or user.role != role:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User not found or role mismatch",
#         )

#     return {"username": user.username, "role": user.role, "id": user.id, "name": user.username}

# # ---------------- DASHBOARD ROUTES ---------------- #
# @router.get("/reception/dashboard", response_class=HTMLResponse)
# async def reception_dashboard(
#     request: Request,
#     current_user: dict = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db)
# ):
#     if current_user["role"] != "reception":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Not authorized to access this resource"
#         )
    
#     # Get today's date and time
#     current_date = datetime.now().strftime("%A, %B %d, %Y")
#     current_time = datetime.now().strftime("%I:%M:%S %p")
#     current_date_iso = datetime.now().strftime("%Y-%m-%d")
#     current_time_24h = datetime.now().strftime("%H:%M")
    
#     # Get stats
#     today_visitors = await crud.get_today_visitors_count(db)
#     waiting_visitors = await crud.get_waiting_visitors_count(db)
#     checked_in_visitors = await crud.get_checked_in_visitors_count(db)
    
#     # Get current visitors
#     current_visitors = await crud.get_current_visitors(db)
    
#     # Get all visitors for all tab
#     all_visitors = await crud.get_all_visitors(db)
    
#     # Prepare visitor data for template
#     processed_current_visitors = []
#     for visitor in current_visitors:
#         initials = "".join([name[0].upper() for name in visitor.name.split()[:2]])
#         processed_current_visitors.append({
#             "id": visitor.id,
#             "name": visitor.name,
#             "email": visitor.email,
#             "company": visitor.company,
#             "host": visitor.host or "Unknown",
#             "checkin_time": visitor.check_in_time.strftime("%I:%M %p") if visitor.check_in_time else "",
#             "duration": str(datetime.now() - visitor.check_in_time).split('.')[0] if visitor.check_in_time else "",
#             "status": visitor.status,
#             "initials": initials
#         })
    
#     # Prepare all visitors data
#     processed_all_visitors = []
#     for visitor in all_visitors:
#         initials = "".join([name[0].upper() for name in visitor.name.split()[:2]])
#         processed_all_visitors.append({
#             "id": visitor.id,
#             "name": visitor.name,
#             "email": visitor.email,
#             "company": visitor.company,
#             "host": visitor.host or "Unknown",
#             "checkin_time": visitor.check_in_time.strftime("%I:%M %p") if visitor.check_in_time else "",
#             "checkout_time": visitor.check_out_time.strftime("%I:%M %p") if visitor.check_out_time else "",
#             "status": visitor.status,
#             "initials": initials
#         })
    
#     # Pagination data
#     pagination = {
#         "start": 1,
#         "end": len(processed_all_visitors),
#         "total": len(processed_all_visitors),
#         "current_page": 1,
#         "pages": 1,
#         "has_prev": False,
#         "has_next": False
#     }
    
#     stats = {
#         "today_visitors": today_visitors,
#         "waiting_visitors": waiting_visitors,
#         "checked_in_visitors": checked_in_visitors
#     }
    
#     # Hardcoded hosts and purposes for now
#     hosts = [
#         {"id": 1, "name": "John Smith", "department": "IT"},
#         {"id": 2, "name": "Sarah Johnson", "department": "HR"},
#         {"id": 3, "name": "Mike Brown", "department": "Finance"},
#         {"id": 4, "name": "Emily Davis", "department": "Marketing"}
#     ]
    
#     purposes = [
#         {"id": 1, "name": "Meeting"},
#         {"id": 2, "name": "Interview"},
#         {"id": 3, "name": "Delivery"},
#         {"id": 4, "name": "Maintenance"},
#         {"id": 5, "name": "Other"}
#     ]
    
#     # reception_dashboard function में context को update करें:
#     return reception_templates.TemplateResponse(
#         "visitor.html",
#         {
#             "request": request,
#             "user": current_user,  # Add this line - template expects 'user' not 'current_user'
#             "current_user": current_user,  # Keep this for other references
#             "current_date": current_date,
#             "current_time": current_time,
#             "current_date_iso": current_date_iso,
#             "current_time_24h": current_time_24h,
#             "stats": stats,
#             "current_visitors": processed_current_visitors,
#             "all_visitors": processed_all_visitors,
#             "hosts": hosts,
#             "purposes": purposes,
#             "pagination": pagination
#         }
#     )







# # ---------------- VISITOR MANAGEMENT ROUTES ---------------- #
# @router.post("/check-in", response_class=RedirectResponse)
# async def check_in_visitor(
#     request: Request,
#     name: str = Form(...),
#     company: str = Form(...),
#     email: Optional[str] = Form(None),
#     phone: str = Form(...),
#     host: str = Form(...),
#     purpose: str = Form(...),
#     notes: Optional[str] = Form(None),
#     current_user: dict = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db)
# ):
#     # Create visitor data
#     visitor_data = {
#         "name": name,
#         "company": company,
#         "email": email,
#         "phone": phone,
#         "host": host,
#         "purpose": purpose,
#         "notes": notes,
#         "status": "Waiting",
#         "check_in_time": datetime.now(),
#         "created_by": current_user["id"]
#     }
    
#     # Create visitor in database
#     visitor = await crud.create_visitor(db, visitor_data)
    
#     # Redirect back to dashboard
#     return RedirectResponse(url="/reception/dashboard", status_code=status.HTTP_302_FOUND)

# @router.post("/visitors/{visitor_id}/check-in", response_class=RedirectResponse)
# async def check_in_existing_visitor(
#     visitor_id: int,
#     current_user: dict = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db)
# ):
#     # Update visitor status to "checked-in"
#     visitor = await crud.update_visitor_status(db, visitor_id, "checked-in")
    
#     # Redirect back to dashboard
#     return RedirectResponse(url="/reception/dashboard", status_code=status.HTTP_302_FOUND)

# @router.post("/visitors/{visitor_id}/check-out", response_class=RedirectResponse)
# async def check_out_visitor(
#     visitor_id: int,
#     current_user: dict = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db)
# ):
#     # Update visitor status to "checked-out" and set checkout time
#     visitor = await crud.check_out_visitor(db, visitor_id)
    
#     # Redirect back to dashboard
#     return RedirectResponse(url="/reception/dashboard", status_code=status.HTTP_302_FOUND)

# @router.get("/visitors/{visitor_id}", response_class=HTMLResponse)
# async def get_visitor_details(
#     request: Request,
#     visitor_id: int,
#     current_user: dict = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db)
# ):
#     # Get visitor details
#     visitor = await crud.get_visitor(db, visitor_id)
    
#     if not visitor:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Visitor not found"
#         )
    
#     # Format visitor data
#     visitor_data = {
#         "id": visitor.id,
#         "name": visitor.name,
#         "company": visitor.company,
#         "email": visitor.email,
#         "phone": visitor.phone,
#         "host": visitor.host,
#         "purpose": visitor.purpose,
#         "checkin_time": visitor.check_in_time.strftime("%Y-%m-%d %H:%M") if visitor.check_in_time else None,
#         "checkout_time": visitor.check_out_time.strftime("%Y-%m-%d %H:%M") if visitor.check_out_time else None,
#         "status": visitor.status,
#         "notes": visitor.notes
#     }
    
#     # Render a detail page
#     return reception_templates.TemplateResponse(
#         "visitor_detail.html",
#         {
#             "request": request,
#             "current_user": current_user,
#             "visitor": visitor_data
#         }
#     )

# @router.post("/visitors/{visitor_id}/update", response_class=RedirectResponse)
# async def update_visitor(
#     visitor_id: int,
#     name: str = Form(...),
#     company: str = Form(...),
#     email: Optional[str] = Form(None),
#     phone: str = Form(...),
#     host: str = Form(...),
#     purpose: str = Form(...),
#     status: str = Form(...),
#     current_user: dict = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db)
# ):
#     # Update visitor details
#     visitor_data = {
#         "name": name,
#         "company": company,
#         "email": email,
#         "phone": phone,
#         "host": host,
#         "purpose": purpose,
#         "status": status
#     }
    
#     visitor = await crud.update_visitor(db, visitor_id, visitor_data)
    
#     if not visitor:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Visitor not found"
#         )
    
#     # Redirect back to dashboard
#     return RedirectResponse(url="/reception/dashboard", status_code=status.HTTP_302_FOUND)

# @router.post("/visitors/{visitor_id}/delete", response_class=RedirectResponse)
# async def delete_visitor(
#     visitor_id: int,
#     current_user: dict = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db)
# ):
#     # Delete visitor
#     success = await crud.delete_visitor(db, visitor_id)
    
#     if not success:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Visitor not found"
#         )
    
#     # Redirect back to dashboard
#     return RedirectResponse(url="/reception/dashboard", status_code=status.HTTP_302_FOUND)

# # ---------------- SEARCH AND FILTER ROUTES ---------------- #
# @router.get("/visitors/search", response_class=HTMLResponse)
# async def search_visitors(
#     request: Request,
#     query: str = Query(..., min_length=1),
#     current_user: dict = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db)
# ):
#     # Search visitors by name, company, or email
#     visitors = await crud.search_visitors(db, query)
    
#     # Format results for template
#     results = []
#     for visitor in visitors:
#         initials = "".join([name[0].upper() for name in visitor.name.split()[:2]])
#         results.append({
#             "id": visitor.id,
#             "name": visitor.name,
#             "company": visitor.company,
#             "email": visitor.email,
#             "host": visitor.host or "Unknown",
#             "checkin_time": visitor.check_in_time.strftime("%I:%M %p") if visitor.check_in_time else None,
#             "status": visitor.status,
#             "initials": initials
#         })
    
#     # Render search results page
#     return reception_templates.TemplateResponse(
#         "visitor_search.html",
#         {
#             "request": request,
#             "current_user": current_user,
#             "visitors": results,
#             "search_query": query
#         }
#     )

# @router.get("/visitors/filter", response_class=HTMLResponse)
# async def filter_visitors(
#     request: Request,
#     status: Optional[str] = Query(None),
#     date_from: Optional[str] = Query(None),
#     date_to: Optional[str] = Query(None),
#     host: Optional[str] = Query(None),
#     current_user: dict = Depends(get_current_user),
#     db: AsyncSession = Depends(get_db)
# ):
#     # Filter visitors based on criteria
#     visitors = await crud.filter_visitors(db, status, date_from, date_to, host)
    
#     # Format results for template
#     results = []
#     for visitor in visitors:
#         initials = "".join([name[0].upper() for name in visitor.name.split()[:2]])
#         results.append({
#             "id": visitor.id,
#             "name": visitor.name,
#             "company": visitor.company,
#             "email": visitor.email,
#             "host": visitor.host or "Unknown",
#             "checkin_time": visitor.check_in_time.strftime("%I:%M %p") if visitor.check_in_time else None,
#             "checkout_time": visitor.check_out_time.strftime("%I:%M %p") if visitor.check_out_time else None,
#             "status": visitor.status,
#             "initials": initials
#         })
    
#     # Render filtered results page
#     return reception_templates.TemplateResponse(
#         "visitor_filter.html",
#         {
#             "request": request,
#             "current_user": current_user,
#             "visitors": results,
#             "filters": {
#                 "status": status,
#                 "date_from": date_from,
#                 "date_to": date_to,
#                 "host": host
#             }
#         }
#     )