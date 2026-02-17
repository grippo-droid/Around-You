from typing import List
from fastapi import APIRouter, Depends, status
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import MessageService
from app.core.dependencies import get_current_user
from app.models.user import UserModel
from app.utils.responses import ResponseModel

router = APIRouter()

@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    message_data: MessageCreate,
    current_user: UserModel = Depends(get_current_user)
):
    message = await MessageService.send_message(str(current_user.id), message_data)
    return ResponseModel.success(data=message, message="Message sent", status_code=201)

@router.get("/{other_user_id}", response_model=List[MessageResponse])
async def get_messages(
    other_user_id: str,
    current_user: UserModel = Depends(get_current_user)
):
    messages = await MessageService.get_messages(str(current_user.id), other_user_id)
    return ResponseModel.success(data=messages)
