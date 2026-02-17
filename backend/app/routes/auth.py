from fastapi import APIRouter, Response, status, Depends
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService
from app.core.dependencies import get_current_user
from app.models.user import UserModel
from app.config.settings import settings
from app.utils.responses import ResponseModel

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    new_user = await AuthService.create_user(user_data)
    return ResponseModel.success(data=new_user, message="User registered successfully")

@router.post("/login")
async def login(response: Response, login_data: UserLogin):
    token = await AuthService.authenticate_user(login_data)
    
    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=token,
        httponly=True,
        max_age=settings.JWT_EXPIRE_MINUTES * 60,
        expires=settings.JWT_EXPIRE_MINUTES * 60,
        secure=True,
        samesite="none"
    )
    
    return ResponseModel.success(data={"access_token": token, "token_type": "bearer"}, message="Login successful")

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(settings.COOKIE_NAME)
    return ResponseModel.success(message="Logged out successfully")

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    return ResponseModel.success(data=current_user)
