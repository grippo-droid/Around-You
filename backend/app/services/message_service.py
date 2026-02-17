from typing import List
from bson import ObjectId
from app.config.database import get_database
from app.models.message import MessageModel
from app.schemas.message import MessageCreate

class MessageService:
    @staticmethod
    async def send_message(sender_id: str, message_data: MessageCreate) -> MessageModel:
        db = get_database()
        new_message = MessageModel(
            sender_id=sender_id,
            receiver_id=message_data.receiver_id,
            content=message_data.content
        )
        result = await db.messages.insert_one(new_message.model_dump(by_alias=True, exclude={"id"}))
        new_message.id = result.inserted_id
        return new_message

    @staticmethod
    async def get_messages(user1_id: str, user2_id: str) -> List[MessageModel]:
        db = get_database()
        cursor = db.messages.find({
            "$or": [
                {"sender_id": user1_id, "receiver_id": user2_id},
                {"sender_id": user2_id, "receiver_id": user1_id}
            ]
        }).sort("timestamp", 1)
        messages = await cursor.to_list(length=100)
        return [MessageModel(**m) for m in messages]
