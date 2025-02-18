from fastapi import APIRouter
from ..model.user_model import User
from ..service.user_service import UserService
from ..auth.auth import Auth

router = APIRouter()
user_service = UserService()
auth = Auth()

@router.put("")
async def validate_user(user: User):
    return await user_service.validate_user(user)
