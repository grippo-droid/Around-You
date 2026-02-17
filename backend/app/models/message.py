from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.utils.object_id import PyObjectId

class MessageModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    sender_id: str
    receiver_id: str
    content: str
    read: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}
