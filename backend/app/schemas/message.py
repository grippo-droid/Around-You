from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.utils.object_id import PyObjectId

class MessageCreate(BaseModel):
    receiver_id: str
    content: str

class MessageResponse(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    sender_id: str
    receiver_id: str
    content: str
    timestamp: datetime

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
