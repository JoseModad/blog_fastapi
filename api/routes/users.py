# Fastapi

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder

# Intern Modules

from ..schemas import User, db
from ..utils import get_password_hash



router = APIRouter(
    tags = ["User Routes"]
)


@router.post("/registration", response_description = "Register a user")
async def registration(user_info: User):
    user_info = jsonable_encoder(user_info)
    
    # check for duplication
    
    username_found = await db["users"].find_one({"name": user_info["name"]})
    email_found = await db["users"].find_one({"email": user_info["email"]})
    
    if username_found:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Username is already taken")
    
    if email_found:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Email id already taken")
    
    # Hash user password
    
    user_info["password"] = get_password_hash(user_info["password"])