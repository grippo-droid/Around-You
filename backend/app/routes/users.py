from fastapi import APIRouter, Depends
from app.schemas.user import UserUpdate, UserResponse
from app.services.user_service import UserService
from app.core.dependencies import get_current_user
from app.models.user import UserModel
from app.utils.responses import ResponseModel

router = APIRouter()

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    update_data: UserUpdate,
    current_user: UserModel = Depends(get_current_user)
):
    updated_user = await UserService.update_user(str(current_user.id), update_data)
    return ResponseModel.success(data=updated_user, message="Profile updated successfully")
