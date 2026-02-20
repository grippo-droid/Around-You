import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# Config from .env
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "around_you_db"

async def debug_direct():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    print(f"Connected to {DB_NAME}")
    
    # 1. Check User
    # User from screenshot is "john doe" or "parth mahale" (from logs) ?
    # The screenshot in Step 2073 shows "john doe".
    # The logs in Step 2035 showed "parth mahale".
    # I'll search for both or list recently created.
    
    print("\n--- Users ---")
    cursor = db.users.find().limit(5).sort("_id", -1)
    async for u in cursor:
        print(f"User: {u.get('name')}, ID: {u['_id']}, Role: {u.get('role')}")
        
        # Check businesses for this user
        count_obj = await db.businesses.count_documents({"owner_id": u['_id']})
        count_str = await db.businesses.count_documents({"owner_id": str(u['_id'])})
        print(f"  -> Businesses (ObjectId): {count_obj}")
        print(f"  -> Businesses (str): {count_str}")

    print("\n--- All Businesses ---")
    b_count = await db.businesses.count_documents({})
    print(f"Total Businesses in DB: {b_count}")
    
    if b_count > 0:
        cursor = db.businesses.find().limit(5)
        async for b in cursor:
            print(f"Business: {b.get('name')}, ID: {b['_id']}, Owner: {b.get('owner_id')} ({type(b.get('owner_id'))})")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(debug_direct())
