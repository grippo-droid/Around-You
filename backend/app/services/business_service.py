from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.config.database import get_database
from app.models.business import BusinessModel
from app.models.user import UserModel
from app.schemas.business import BusinessCreate, BusinessUpdate

class BusinessService:
    @staticmethod
    async def create_business(owner_id: str, business_data: BusinessCreate) -> BusinessModel:
        db = get_database()
        new_business = BusinessModel(
            owner_id=owner_id,
            **business_data.model_dump()
        )
        result = await db.businesses.insert_one(new_business.model_dump(by_alias=True, exclude={"id"}))
        new_business.id = result.inserted_id
        return new_business

    @staticmethod
    async def get_businesses(category: Optional[str] = None, search: Optional[str] = None) -> List[BusinessModel]:
        db = get_database()
        query = {}
        if category:
            query["category"] = category
        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}},
                {"category": {"$regex": search, "$options": "i"}}
            ]
        
        cursor = db.businesses.find(query).sort("created_at", -1)
        businesses = await cursor.to_list(length=100)
        return [BusinessModel(**b) for b in businesses]

    @staticmethod
    async def get_business_by_id(business_id: str) -> Optional[BusinessModel]:
        db = get_database()
        if not ObjectId.is_valid(business_id):
            return None
        doc = await db.businesses.find_one({"_id": ObjectId(business_id)})
        if doc:
            return BusinessModel(**doc)
        return None

    @staticmethod
    async def get_my_businesses(owner_id: str) -> List[BusinessModel]:
        db = get_database()
        cursor = db.businesses.find({"owner_id": owner_id})
        businesses = await cursor.to_list(length=100)
        return [BusinessModel(**b) for b in businesses]
    @staticmethod
    async def delete_business(business_id: str, owner_id: str) -> bool:
        db = get_database()
        if not ObjectId.is_valid(business_id):
            return False
            
        result = await db.businesses.delete_one({
            "_id": ObjectId(business_id),
            "owner_id": owner_id
        })
        return result.deleted_count > 0

    @staticmethod
    async def update_business(business_id: str, owner_id: str, business_data: BusinessUpdate) -> Optional[BusinessModel]:
        db = get_database()
        if not ObjectId.is_valid(business_id):
            return None
            
        update_data = {k: v for k, v in business_data.model_dump().items() if v is not None}
        
        if not update_data:
            return await BusinessService.get_business_by_id(business_id)

        result = await db.businesses.update_one(
            {"_id": ObjectId(business_id), "owner_id": owner_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            # Check if it was a match but no modification (still success) or no match
            matched = await db.businesses.find_one({"_id": ObjectId(business_id), "owner_id": owner_id})
            if not matched:
                return None
                
        return await BusinessService.get_business_by_id(business_id)

        return await BusinessService.get_business_by_id(business_id)

    @staticmethod
    async def add_staff(business_id: str, owner_id: str, name: str, phone: str, designation: str) -> bool:
        db = get_database()
        if not ObjectId.is_valid(business_id):
            return False
            
        staff_member = {
            "id": str(ObjectId()),
            "name": name,
            "phone": phone,
            "designation": designation,
            "joined_at": datetime.utcnow()
        }
        
        # Add to business staff list
        result = await db.businesses.update_one(
            {"_id": ObjectId(business_id), "owner_id": owner_id},
            {"$push": {"staff": staff_member}}
        )
        return result.modified_count > 0

    @staticmethod
    async def remove_staff(business_id: str, owner_id: str, staff_id: str) -> bool:
        db = get_database()
        if not ObjectId.is_valid(business_id):
            return False

        result = await db.businesses.update_one(
            {"_id": ObjectId(business_id), "owner_id": owner_id},
            {"$pull": {"staff": {"id": staff_id}}}
        )
        return result.modified_count > 0

    @staticmethod
    async def get_business_staff(business_id: str) -> List[dict]:
        db = get_database()
        if not ObjectId.is_valid(business_id):
            return []
            
        business = await db.businesses.find_one({"_id": ObjectId(business_id)})
        if not business or "staff" not in business:
            return []
            
        return business["staff"]
