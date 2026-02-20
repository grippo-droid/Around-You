import asyncio
from app.config.database import get_database
from app.models.user import UserModel
from bson import ObjectId

async def debug_user_businesses():
    db = get_database()
    
    # 1. Find user "john doe" or similar
    # Adjust the regex if needed, or just list all users to find the right one if "john doe" is generic
    user = await db.users.find_one({"name": {"$regex": "john doe", "$options": "i"}})
    
    if not user:
        print("User 'john doe' not found.")
        # List first 5 users to help identify
        cursor = db.users.find().limit(5)
        async for u in cursor:
            print(f"User: {u['name']}, ID: {u['_id']}, Role: {u.get('role')}")
        return

    print(f"Found User: {user['name']}")
    print(f"User ID: {user['_id']}")
    print(f"User Role: {user.get('role')}")

    user_id = user['_id']

    # 2. Count businesses
    count = await db.businesses.count_documents({"owner_id": user_id})
    print(f"Business Count in DB for owner_id {user_id}: {count}")

    # 3. List businesses
    cursor = db.businesses.find({"owner_id": user_id})
    async for b in cursor:
        print(f"Business: {b['name']}, ID: {b['_id']}, Owner ID: {b['owner_id']}")

    # 4. Check for string vs ObjectId mismatch
    # Sometimes owner_id is stored as string in one place and ObjectId in another
    count_str = await db.businesses.count_documents({"owner_id": str(user_id)})
    print(f"Business Count in DB for owner_id (string) {user_id}: {count_str}")

if __name__ == "__main__":
    import sys
    import os
    # Add backend directory to sys.path to allow imports
    sys.path.append(os.path.join(os.getcwd(), 'backend'))
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(debug_user_businesses())
