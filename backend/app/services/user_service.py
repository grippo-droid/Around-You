from typing import Optional
from bson import ObjectId
from app.config.database import get_database
from app.models.user import UserModel
from app.schemas.user import UserUpdate

class UserService:
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[UserModel]:
        db = get_database()
        user_doc = await db.users.find_one({"_id": ObjectId(user_id)})
        if user_doc:
            return UserModel(**user_doc)
        return None

    @staticmethod
    async def update_user(user_id: str, update_data: UserUpdate) -> Optional[UserModel]:
        db = get_database()
        update_dict = update_data.model_dump(exclude_unset=True)
        if not update_dict:
            return await UserService.get_user_by_id(user_id)

        await db.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_dict}
        )
        return await UserService.get_user_by_id(user_id)
