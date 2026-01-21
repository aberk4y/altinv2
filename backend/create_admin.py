
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from auth_service import get_password_hash
from dotenv import load_dotenv

load_dotenv('.env')

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'berkay_altin_db')

async def create_admin():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    username = "admin"
    password = "admin123" # Initial password
    
    hashed_password = get_password_hash(password)
    
    user_doc = {
        "username": username,
        "hashed_password": hashed_password,
        "is_active": True,
        "role": "admin"
    }
    
    # Upsert admin user
    result = await db.users.update_one(
        {"username": username},
        {"$set": user_doc},
        upsert=True
    )
    
    if result.upserted_id:
        print(f"Admin user created. ID: {result.upserted_id}")
    else:
        print("Admin user updated.")
        
    print(f"Username: {username}")
    print(f"Password: {password}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin())
