# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from sqlalchemy.ext.asyncio import AsyncSession
# from jose import JWTError, jwt
# from typing import Optional
# from app import crud, models
# from app.database import get_db
# from app.security import verify_password
# import os




# SECRET_KEY = os.getenv("SECRET_KEY", "logan")
# ALGORITHM = "HS256"

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# async def authenticate_user(db: AsyncSession, username: str, password: str) -> Optional[models.User]:
#     user = await crud.get_user_by_username(db, username)
#     if not user:
#         return None
#     if not verify_password(password, user.password_hash):
#         return None
#     return user


# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: AsyncSession = Depends(get_db)
# ) -> models.User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception

#     user = await crud.get_user_by_username(db, username=username)
#     if user is None:
#         raise credentials_exception
#     return user




from fastapi import Depends, Cookie,Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from sqlalchemy.future import select

from app.security import ALGORITHM, SECRET_KEY
from datetime import timedelta, datetime
from app.database import get_db
from typing import Optional
from app.models import User





# Remove these lines as they're already in security.py
SECRET_KEY = "logan"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")






# async def get_current_user(
#     request: Request,
#     db: AsyncSession = Depends(get_db),
#     access_token: Optional[str] = Cookie(None)
# ):
#     token = access_token
#     if not token:
#         auth_header = request.headers.get("Authorization")
#         if auth_header and auth_header.startswith("Bearer "):
#             token = auth_header[7:]

#     if not token:
#         return None

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         role: str = payload.get("role")
#         if not username or not role:
#             return None
#     except JWTError:
#         return None

#     result = await db.execute(select(User).where(User.username == username))
#     user = result.scalars().first()
#     if not user or user.role != role:
#         return None

#     # ✅ Return with id
#     return {"id": user.id, "username": user.username, "role": user.role}





async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
    access_token: Optional[str] = None  # ✅ Plain str rakho
):
    # ✅ Extract token from cookie manually
    token = request.cookies.get("access_token") or access_token

    if not token:
        # Try Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header[7:]

    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if not username or not role:
            return None
    except JWTError:
        return None

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user or user.role != role:
        return None

    return {"id": user.id, "username": user.username, "role": user.role}


    


    