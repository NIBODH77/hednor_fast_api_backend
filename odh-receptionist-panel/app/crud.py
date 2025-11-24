from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import func
from app import models, schemas
from sqlalchemy.future import select
from passlib.context import CryptContext
from app.models import Visitor



from app.models import User
from sqlalchemy.future import select
from datetime import date
from datetime import timedelta
from datetime import datetime






pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')[:72]
    return pwd_context.hash(password_bytes)


# =========================================Login and User Management =========================================

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        password_hash=hash_password(user.password),
        role=user.role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_users(db: AsyncSession):
    result = await db.execute(select(models.User))
    return result.scalars().all()




# =======================================Receptionist Dashboard Management ================================




# Get recent visitors (last 10)
async def get_recent_visitors(db, limit: int = 15):
    result = await db.execute(
        select(Visitor).order_by(Visitor.check_in_time.desc()).limit(limit)
    )
    return result.scalars().all()

    # ---------------- Total visitors --------------------------
    result = await db.execute(sa.select(func.count(Visitor.id)))
    total_visitors = result.scalar() or 0   # ✅ count of ALL visitors


# Aaj ke total visitors


# ✅ Count today's visitors
# async def count_today_visitors(db: AsyncSession):
#     today = date.today()
#     tomorrow = today + timedelta(days=1)
#     result = await db.execute(
#         select(func.count()).select_from(Visitor).where(
#             Visitor.check_in_time >= today,
#             Visitor.check_in_time < tomorrow
#         )
#     )
#     count = result.scalar() or 0
#     print("DEBUG: Today's visitors =", count)
#     return count



async def count_today_visitors(db: AsyncSession):
    today = datetime.combine(date.today(), datetime.min.time())   # आज का 00:00:00
    tomorrow = today + timedelta(days=1)                          # कल का 00:00:00

    result = await db.execute(
        select(func.count())
        .select_from(Visitor)
        .where(
            Visitor.check_in_time >= today,
            Visitor.check_in_time < tomorrow
        )
    )
    count = result.scalar() or 0
    print("DEBUG: Today's visitors =", count)
    return count





# ==========================================Receptionist Visitor Management ==========================================





# ---------- CRUD operations ----------
# 🔹 Create new visitor (status = "Waiting" by default)
async def create_visitor(db: AsyncSession, name: str, company: str, host: str, purpose: str):
    new_visitor = Visitor(
        name=name,
        company=company,
        host=host,
        purpose=purpose,
        status="Waiting"   # ✅ Start with Waiting
    )
    db.add(new_visitor)
    await db.commit()
    await db.refresh(new_visitor)
    return new_visitor




# 🔹 1. Current Visitors (today check-in but not checked-out)


# 🔹 2. All Visitors

# ✅ Get all visitors
async def get_all_visitors(db: AsyncSession):
    result = await db.execute(select(models.Visitor))
    return result.scalars().all()

# ✅ Create visitor
async def create_visitor(db: AsyncSession, visitor_data: dict):
    visitor = models.Visitor(**visitor_data)
    db.add(visitor)
    await db.commit()
    await db.refresh(visitor)
    return visitor




# ======================================  Pagination For Admin User =============================================




# In your crud.py file
async def get_users_paginated(db: AsyncSession, page: int = 1, per_page: int = 10):
    # Count total users
    total_users_result = await db.execute(select(func.count(User.id)))
    total_users = total_users_result.scalar()
    total_pages = (total_users + per_page - 1) // per_page
    
    # Get paginated users
    offset = (page - 1) * per_page
    result = await db.execute(select(User).offset(offset).limit(per_page))
    users = result.scalars().all()
    
    return users, total_pages