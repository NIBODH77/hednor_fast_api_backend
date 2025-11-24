from passlib.context import CryptContext
from datetime import datetime
from typing import Dict

from fastapi import HTTPException
import httpx
import re
from app.settings import Settings
from app.schemas import SMSRequest  # Add this import if SMSRequest is defined in schemas.py
from pydantic_settings import BaseSettings
import random
import time
from starlette.requests import Request
from app.models import OTP, Visitor
from sqlalchemy.ext.asyncio import AsyncSession
import random, sqlalchemy as sa





pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# session key where we store flashes
# FLASH_KEY = "_flashes"  







def get_password_hash(password: str) -> str:
    # Bcrypt only supports passwords up to 72 bytes
    password_bytes = password.encode('utf-8')[:72]
    return pwd_context.hash(password_bytes)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Bcrypt only supports passwords up to 72 bytes
    password_bytes = plain_password.encode('utf-8')[:72]
    return pwd_context.verify(password_bytes, hashed_password)





# ✅ Date & Time context (frontend ke liye)
def now_ctx() -> Dict[str, str]:
    now = datetime.now()
    return {
        "current_date": now.strftime("%A, %B %d, %Y"),
        "current_time": now.strftime("%I:%M %p"),
    }


# ✅ Simple pagination helper
def pagination(total: int, page: int, per_page: int):
    pages = (total // per_page) + (1 if total % per_page > 0 else 0)
    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": pages,
        "has_next": page < pages,
        "has_prev": page > 1,
    }

def stats_from_visitors(visitors):
    return {
        "today_visitors": len(visitors),
        "waiting_visitors": len([v for v in visitors if v.status == "pending"]),
        "checked_in_visitors": len([v for v in visitors if v.status == "checked-in"]),
    }



# =================================== Helper function for All  visitor data ================================


def add_initials(visitor):
    visitor.initials = "".join([p[0].upper() for p in visitor.name.split() if p])[:2]
    return visitor

def with_initials(visitors):
    return [add_initials(v) for v in visitors]








# ======================================== Masked function for security purpuse =================================


def mask_name(name: str) -> str:
    if not name:
        return ""

    parts = name.split(" ")

    masked_parts = []
    for part in parts:
        if len(part) <= 2:
            # अगर word छोटा है तो पूरा word ही दिखा दो
            masked_parts.append(part)
        else:
            # पहले 3 char दिखाओ, बाकी सब *
            masked_parts.append(part[:2] + "*" * (len(part) - 2))

    return " ".join(masked_parts)



def mask_phone(phone: str) -> str:
    if not phone:
        return ""
    phone = phone.strip()
    return phone[:5] + "*****" if len(phone) > 5 else "*" * len(phone)


def mask_email(email: str) -> str:
    if not email or "@" not in email:
        return ""
    local, domain = email.split("@", 1)
    return "*****@" + domain


def get_initials(name: str) -> str:
    if not name:
        return ""
    return "".join([p[0].upper() for p in name.split()[:2]])  # Max 2 letters

def mask_address(address: str) -> str:
    if not address:
        return ""
    return "******"



async def generate_and_store_otp(db: AsyncSession, phone: str):
    """
    Generate a 6-digit OTP and keep only one OTP in the table.
    Deletes any old OTP and stores the new one.
    """
    # OTP generate karo
    otp_code = str(random.randint(100000, 999999))

    # Purane sabhi OTP delete karo
    # await db.execute(sa.delete(OTP))

    # Visitor find karo
    result = await db.execute(
        sa.select(Visitor)
        .where(Visitor.phone == phone)
        .order_by(Visitor.check_in_time.desc())
        .limit(1)
    )
    visitor = result.scalar_one_or_none()

    # Naya OTP insert karo
    new_otp = OTP(
        otp_code=otp_code,
        visitor_id=visitor.id if visitor else None,
        
    )
    db.add(new_otp)

    await db.commit()
    await db.refresh(new_otp)

    return otp_code





# async def generate_and_store_otp(db: AsyncSession, phone: str):
#     """
#     Generate a 6-digit OTP and store in DB. Only one OTP per visitor exists.
#     """
#     # 1. Visitor ko phone se dhundo
#     result = await db.execute(
#         sa.select(Visitor)
#         .where(Visitor.phone == phone)
#         .order_by(Visitor.check_in_time.desc())  # latest visitor
#         .limit(1)
#     )
#     visitor = result.scalar_one_or_none()
#     if not visitor:
#         raise HTTPException(status_code=404, detail="Visitor not found with this phone number")

#     # 2. OTP generate karo
#     otp_code = str(random.randint(100000, 999999))

#     # 3. Purane OTP delete karo is visitor ke liye
#     await db.execute(sa.delete(OTP).where(OTP.visitor_id == visitor.id))

#     # 4. Naya OTP insert karo
#     new_otp = OTP(
#         otp_code=otp_code,
#         visitor_id=visitor.id
#     )
#     db.add(new_otp)
#     await db.commit()
#     await db.refresh(new_otp)

#     return otp_code



# async def generate_and_store_otp(db: AsyncSession, phone: str):
#     """
#     Generate a 6-digit OTP and keep only one OTP in the table at a time.
#     Deletes any old OTP and stores the new one.
#     """

#     # 1. Visitor ko phone se dhundo
#     result = await db.execute(
#         sa.select(Visitor)
#         .where(Visitor.phone == phone)
#         .order_by(Visitor.check_in_time.desc())
#         .limit(1)
#     )
#     visitor = result.scalar_one_or_none()

#     # 2. OTP generate karo
#     otp_code = str(random.randint(100000, 999999))

#     # 3. Purane OTP delete karo (sabhi purane delete ho jayenge)
#     await db.execute(sa.delete(OTP))

#     # 4. Naya OTP insert karo (visitor ho to uska id, nahi to None)
#     new_otp = OTP(
#         otp_code=otp_code,
#         visitor_id=visitor.id if visitor else None
#     )
#     db.add(new_otp)

#     await db.commit()
#     await db.refresh(new_otp)

#     return otp_code





# async def verify_and_delete_otp(db: AsyncSession, visitor_id: int, otp: str) -> bool:
#     result = await db.execute(
#         sa.select(OTP).where(OTP.visitor_id == visitor_id, OTP.otp_code == int(otp))
#     )
#     otp_entry = result.scalar_one_or_none()

#     if not otp_entry:
#         return False

#     # ✅ Valid OTP → delete
#     await db.delete(otp_entry)
#     await db.commit()
#     return True


async def verify_otp(db: AsyncSession, phone: str, otp: str) -> bool:
    result = await db.execute(
        sa.select(Visitor).where(Visitor.phone == phone).order_by(Visitor.check_in_time.desc()).limit(1)
    )
    visitor = result.scalar_one_or_none()

    if visitor:
        result = await db.execute(
            sa.select(OTP).where(OTP.visitor_id == visitor.id, OTP.otp_code == otp)
        )
    else:
        result = await db.execute(
            sa.select(OTP).where(OTP.visitor_id.is_(None), OTP.otp_code == otp)
        )

    otp_obj = result.scalar_one_or_none()
    if not otp_obj:
        return False

    # ✅ mark as verified instead of deleting
    otp_obj.is_verified = True
    db.add(otp_obj)
    await db.commit()
    await db.refresh(otp_obj)

    return True




# async def _send_to_gateway(payload: SMSRequest, settings: Settings, db: AsyncSession, visitor: Visitor):
#     # Build query exactly like your working URL


    

#     # DLT_REGISTER_OTP = (
#     # "Dear {user} , Your OTP for ODH Developers registration is {otp} . "
#     # "It is valid for 5 minutes. Don't share your OTP with anyone."
#     # )
#     # msg = DLT_REGISTER_OTP.format(user="user", otp=generate_otp(payload.mobile))


#     # Step 1: Generate & store OTP in DB
#     otp = await generate_and_store_otp(db, visitor)

#     # Step 2: Create message using that OTP
#     DLT_REGISTER_OTP = (
#         "Dear User , Your OTP for ODH Developers registration is {otp}. "
#         "It is valid for 5 minutes. Don't share your OTP with anyone."
#     )
#     msg = DLT_REGISTER_OTP.format( otp=otp)

#     params={
#         "userid": "vprlst",
#         "password": "Odh@87612",
#         "sendMethod": payload.sendMethod,
#         "mobile": re.sub(r"\D", "", payload.mobile),
#         "msg": msg,
#         "senderid": payload.senderid or settings.SMSGW_SENDERID or "",
#         # "test": "true" if payload.test else "false",
#         "msgType": payload.msgType,
#         **({"dltEntityId": ''} if payload.dltEntityId is not None else {}),
#         **({"dltTemplateId": payload.dltTemplateId} if payload.dltTemplateId is not None else {}),
#         "duplicatecheck": "true" if payload.duplicatecheck else "false",
#         "output": "json",
#     }
#     # if payload.dltEntityId is not None:
#     #     params["dltEntityId"] = payload.dltEntityId
#     # if payload.dltTemplateId is not None:
#     #     params["dltTemplateId"] = payload.dltTemplateId

#     try:
#         async with httpx.AsyncClient(timeout=30) as client:
#             # use GET with params (your working example is a GET querystring)
#             # resp = await client.get(settings.SMSGW_BASE_URL, params=params)
#             req = client.build_request("GET", settings.SMSGW_BASE_URL, params=params)
#             built_url = str(req.url).replace("%40", "@")  # for readability in logs
#             print("SMS full URL:", built_url)
#             # print("SMS built URL:", _mask_query(built_url))

#             # Send
#             resp = await client.send(req)

#     except httpx.RequestError as e:
#         raise HTTPException(status_code=504, detail=f"SMS provider unreachable: {e!s}")

#     # Try to parse JSON even if content-type is wrong
#     try:
#         provider_json = resp.json()
#     except Exception:
#         provider_json = {"raw": resp.text}

#     # Non-2xx -> bubble up with details (no secrets included)
#     if resp.status_code >= 400:
#         raise HTTPException(
#             status_code=502,
#             detail={
#                 "provider": "smsgateway.center",
#                 "status_code": resp.status_code,
#                 "response": provider_json,
#             },
#         )

#     # Some gateways return 200 but include failure codes in body
#     err_code = str(provider_json.get("ErrorCode") or provider_json.get("errorCode") or "")
#     status_flag = str(provider_json.get("Status") or provider_json.get("status") or "").lower()
#     if (err_code and err_code != "0") or status_flag in {"error", "failed", "failure"}:
#         raise HTTPException(
#             status_code=502,
#             detail={
#                 "provider": "smsgateway.center",
#                 "error_code": err_code or status_flag or None,
#                 "response": provider_json,
#             },
#         )

#     return {
#         "ok": True,
#         "provider": "smsgateway.center",
#         "response": provider_json,
#     }



async def _send_to_gateway(payload: SMSRequest, settings: Settings, db: AsyncSession, visitor):
    """
    Send OTP SMS to given visitor (or just mobile number).
    """
    # ✅ Step 1: Generate OTP
    otp = await generate_and_store_otp(db, visitor.phone)

    # ✅ Step 2: Build SMS text


    DLT_REGISTER_OTP = (
        "Dear User , Your OTP for ODH Developers registration is {otp}. "
        "It is valid for 5 minutes. Don't share your OTP with anyone."
    )

    msg = DLT_REGISTER_OTP.format( otp=otp)


    # ✅ Step 3: Prepare params for SMS gateway
    params = {
        "userid": "vprlst",
        "password": "Odh@87612",
        "sendMethod": payload.sendMethod or "quick",
        "mobile": re.sub(r"\D", "", payload.mobile),  # sanitize mobile
        "msg": msg,
        "senderid": payload.senderid or settings.SMSGW_SENDERID or "ODHGRP",
        "msgType": payload.msgType or "text",
        "duplicatecheck": "true",
        "output": "json",
    }

    # ✅ Step 4: Send request
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            req = client.build_request("GET", settings.SMSGW_BASE_URL, params=params)
            built_url = str(req.url).replace("%40", "@")
            print("📨 SMS full URL:", built_url)

            resp = await client.send(req)

    except httpx.RequestError as e:
        raise HTTPException(status_code=504, detail=f"SMS provider unreachable: {e!s}")

    # ✅ Step 5: Handle response
    try:
        provider_json = resp.json()
    except Exception:
        provider_json = {"raw": resp.text}

    if resp.status_code >= 400:
        raise HTTPException(
            status_code=502,
            detail={"provider": "smsgateway.center", "status_code": resp.status_code, "response": provider_json},
        )

    err_code = str(provider_json.get("ErrorCode") or provider_json.get("errorCode") or "")
    status_flag = str(provider_json.get("Status") or provider_json.get("status") or "").lower()
    if (err_code and err_code != "0") or status_flag in {"error", "failed", "failure"}:
        raise HTTPException(
            status_code=502,
            detail={"provider": "smsgateway.center", "error_code": err_code or status_flag or None, "response": provider_json},
        )

    return {"ok": True, "provider": "smsgateway.center", "response": provider_json}



# async def _send_to_gateway(payload: SMSRequest, settings: Settings, db: AsyncSession, visitor):
#     """
#     Send OTP SMS to given visitor (or just mobile number).
#     """
#     # ✅ Step 1: Generate OTP
#     otp = await generate_and_store_otp(db, visitor.phone)

#     # ✅ Step 2: Build SMS text


#     DLT_REGISTER_OTP = (
#         "Dear User , Your OTP for ODH Developers registration is {otp}. "
#         "It is valid for 5 minutes. Don't share your OTP with anyone."
#     )
#     msg = DLT_REGISTER_OTP.format( otp=otp)


#     # ✅ Step 3: Prepare params for SMS gateway
#     params = {
#         "userid": "vprlst",
#         "password": "Odh@87612",
#         "sendMethod": payload.sendMethod or "quick",
#         "mobile": re.sub(r"\D", "", payload.mobile),  # sanitize mobile
#         "msg": msg,
#         "senderid": payload.senderid or settings.SMSGW_SENDERID or "ODHGRP",
#         "msgType": payload.msgType or "text",
#         "duplicatecheck": "true",
#         "output": "json",
#     }

#     # ✅ Step 4: Send request
#     try:
#         async with httpx.AsyncClient(timeout=30) as client:
#             req = client.build_request("GET", settings.SMSGW_BASE_URL, params=params)
#             built_url = str(req.url).replace("%40", "@")
#             print("📨 SMS full URL:", built_url)

#             resp = await client.send(req)

#     except httpx.RequestError as e:
#         raise HTTPException(status_code=504, detail=f"SMS provider unreachable: {e!s}")

#     # ✅ Step 5: Handle response
#     try:
#         provider_json = resp.json()
#     except Exception:
#         provider_json = {"raw": resp.text}

#     if resp.status_code >= 400:
#         raise HTTPException(
#             status_code=502,
#             detail={"provider": "smsgateway.center", "status_code": resp.status_code, "response": provider_json},
#         )

#     err_code = str(provider_json.get("ErrorCode") or provider_json.get("errorCode") or "")
#     status_flag = str(provider_json.get("Status") or provider_json.get("status") or "").lower()
#     if (err_code and err_code != "0") or status_flag in {"error", "failed", "failure"}:
#         raise HTTPException(
#             status_code=502,
#             detail={"provider": "smsgateway.center", "error_code": err_code or status_flag or None, "response": provider_json},
#         )

#     return {"ok": True, "provider": "smsgateway.center", "response": provider_json}




# ========================= FLASH MSG =========================
FLASH_KEY = "_flashes"

def flash(request: Request, message: str, category: str = "info") -> None:
    if not hasattr(request, "session"):
        raise RuntimeError("SessionMiddleware not configured.")
    flashes = request.session.get(FLASH_KEY, [])
    print("==========",flashes)

    flashes.append({"message": str(message), "category": str(category)})
    request.session[FLASH_KEY] = flashes


def get_flashed_messages(request: Request, with_categories: bool = True):
    if not hasattr(request, "session"):
        return []
    flashes = request.session.pop(FLASH_KEY, [])
    print("====++++++++======",flashes)
    if with_categories:
        print("====++++++++======",flashes)

        return [(f["category"], f["message"]) for f in flashes]
    return [f["message"] for f in flashes]




# def flash(request, message: str, category: str = "info"):
#     if "_flashes" not in request.session:
#         request.session["_flashes"] = []
#     request.session["_flashes"].append((category, message))


# def get_flashed_messages(request, with_categories: bool = False):
#     flashes = request.session.pop("_flashes", [])
#     if with_categories:
#         return flashes
#     return [msg for cat, msg in flashes]
