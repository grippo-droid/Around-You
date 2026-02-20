from pymongo import MongoClient
from bson import ObjectId
import sys

# Config from .env
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "around_you_db"

def debug_sync():
    print("Starting debug_sync...")
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        print(f"Connected to {DB_NAME}")
        
        print("\n--- Users ---")
        users = list(db.users.find().limit(5).sort("_id", -1))
        for u in users:
            print(f"User: {u.get('name')}, ID: {u['_id']}, Role: {u.get('role')}")
            
            # Check businesses for this user
            count_obj = db.businesses.count_documents({"owner_id": u['_id']})
            count_str = db.businesses.count_documents({"owner_id": str(u['_id'])})
            print(f"  -> Businesses (ObjectId): {count_obj}")
            print(f"  -> Businesses (str): {count_str}")

        print("\n--- All Businesses ---")
        b_count = db.businesses.count_documents({})
        print(f"Total Businesses in DB: {b_count}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_sync()
