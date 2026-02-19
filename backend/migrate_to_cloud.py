import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path
import certifi

# Load environment variables (for local DB)
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# CONFIG
LOCAL_MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
LOCAL_DB_NAME = os.environ.get('DB_NAME', 'berkay_altin_db')

# CLOUD CONFIG (From User)
CLOUD_MONGO_URL = "mongodb+srv://berkayaras098_db_user:VVC67pJ3iW3n4BBr@altinberkay.9jsugfx.mongodb.net/?appName=Altinberkay"
CLOUD_DB_NAME = "berkay_altin_db" # We use the same name or let connection string decide

async def migrate():
    print(f"Connecting to LOCAL DB: {LOCAL_MONGO_URL}...")
    local_client = AsyncIOMotorClient(LOCAL_MONGO_URL)
    local_db = local_client[LOCAL_DB_NAME]
    
    print(f"Connecting to CLOUD DB...")
    # tlsCAFile is needed for some environments, usually automatic but good for safety
    cloud_client = AsyncIOMotorClient(CLOUD_MONGO_URL, tlsCAFile=certifi.where())
    cloud_db = cloud_client[CLOUD_DB_NAME]
    
    # 1. Migrate Users (Admin account)
    print("Migrating 'users'...")
    users = await local_db.users.find({}).to_list(1000)
    if users:
        # Clear existing? Or update? Let's upsert by username
        for user in users:
            # remove _id to let cloud generate one or keep it? Keeping it is fine if empty target.
            # safe approach: upsert by username
            await cloud_db.users.update_one(
                {"username": user["username"]},
                {"$set": user},
                upsert=True
            )
        print(f"Migrated {len(users)} users.")
    else:
        print("No users found locally.")

    # 2. Migrate Margins
    print("Migrating 'margins'...")
    margins = await local_db.margins.find({}).to_list(1000)
    if margins:
        for margin in margins:
            await cloud_db.margins.update_one(
                {"product_name_key": margin["product_name_key"]},
                {"$set": margin},
                upsert=True
            )
        print(f"Migrated {len(margins)} margins.")
    else:
        print("No margins found locally.")
        
    local_client.close()
    cloud_client.close()
    print("Migration Complete! Cloud DB is ready.")

if __name__ == "__main__":
    asyncio.run(migrate())
