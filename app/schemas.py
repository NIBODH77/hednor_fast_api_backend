from typing import Optional,Literal
from datetime import datetime
from pydantic import BaseModel, EmailStr,field_validator, conint



# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: str = "receptionist"

class UserCreate(UserBase):
    password: str
    role: str = "receptionist"  # Make sure this line exists
    created_at: datetime


class User(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True

    
# class UserUpdate(UserBase):
#     password: Optional[str] = None
#     username: Optional[str] = None
#     email: Optional[EmailStr] = None
#     full_name: Optional[str] = None
#     role: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password_hash: Optional[str] = None
    role: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    password_hash:str
    role: str

    class Config:
        from_attributes = True



ALLOWED_PHONENUM_VALIDATION=conint(ge=1000000000, le=9999999999) 

class VisitorBase(BaseModel):
    
    name: str
    company: Optional[str] = None
    # email: Optional[EmailStr] = None
    # phone: Optional[str] = None
    phone:str=ALLOWED_PHONENUM_VALIDATION

    host: Optional[str] = None
    purpose: Optional[str] = None
    state: Optional[str] = None     # ✅ added
    city: Optional[str] = None      # ✅ added
    status: str = "checked-in"


class VisitorCreate(VisitorBase):
    pass

class Visitor(VisitorBase):
    id: int
    status: str
    check_in_time: datetime
    check_out_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class VisitorUpdate(VisitorBase):
    name: Optional[str] = None
    status: Optional[str] = None
    state: Optional[str] = None     # ✅ added
    city: Optional[str] = None      # ✅ added
    check_out_time: Optional[datetime] = None   # ✅ added



# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    username: Optional[str] = None

# Dashboard Schemas
class DashboardStats(BaseModel):
    today_visitors: int
    waiting: int
    checked_in: int


# ===================== SMS SEND ==========================


class SMSRequest(BaseModel):
    visitor_id: Optional[int] = None   # ✅ now optional
    mobile: str
    msg: str
    senderid: Optional[str] = None
    dltEntityId: Optional[str] = None
    dltTemplateId: Optional[str] = None
    msgType: str = "text"
    sendMethod: str = "quick"
    duplicatecheck: bool = False
    test: bool = False

    @field_validator("mobile")
    @classmethod
    def clean_mobile(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("mobile is required")
        return v



ALLOWED_OTP_VALIDATION =conint(ge=100000, le=999999) 

# ---------- OTP Schemas ----------
class OTPBase(BaseModel):
    otp_code: str=(ALLOWED_OTP_VALIDATION)  # 6 digit OTP


class OTPCreate(OTPBase):
    visitor_id: str


class OTPResponse(OTPBase):
    id: int
    visitor_id: str

    class Config:
        from_attributes = True


# ✅ Request body
class VerifyOTPRequest(BaseModel):
    phone: str
    otp_code: str



# class CheckInRequest(BaseModel):
#     phone: str
#     otp: str   # ✅ required
#     name: str
#     company: Optional[str]
#     email: Optional[str]
#     host: str
#     purpose: str
#     address: Optional[str]
#     date: str
#     time: str

