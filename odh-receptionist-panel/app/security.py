from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
import os
from sqlalchemy import select
from app.models import User






# Security config
SECRET_KEY = os.getenv("SECRET_KEY", "logan")[:72]  # Limit to 72 bytes for bcrypt
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")





# # Auth
# async def authenticate_user(db: AsyncSession, username: str, password: str):
#     user = await crud.get_user_by_username(db, username)
#     if not user:
#         return None
#     if not verify_password(password, user.hashed_password):  # make sure model column = hashed_password
#         return None
#     return user




def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt





def get_password_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')[:72]
    return pwd_context.hash(password_bytes)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        result = pwd_context.verify(plain_password, hashed_password)
        print(f"Password verification: {result}")
        return result
    except Exception as e:
        print(f"Password verification error: {e}")
        return False




def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None



# Authenticate user
async def authenticate_user(db: AsyncSession, username: str, password: str):
    print("came to authenticate")
    result = await db.execute(select(User).where(User.username == username))
    print("----------------",result)
    user = result.scalars().first()
    print("users is",user)
    if not user:
        return None
    if not verify_password(password, user.password_hash):  # column fix
        print("password not verified")
        return None
    return user





def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise Exception("Token has expired")
    except JWTError:
        raise Exception("Invalid token")

def get_username_from_token(token: str) -> str:
    payload = decode_access_token(token)
    username: str = payload.get("sub")
    if not username:
        raise Exception("Invalid token: no subject found")
    return username

def validate_token(token: str) -> bool:
    try:
        decode_access_token(token)
        return True
    except Exception:
        return False


def getJWTDetail():

    return SECRET_KEY,ALGORITHM