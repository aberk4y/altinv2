import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def migrate_margins():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Migrating margins to include is_visible=True...")
    # Update all documents where is_visible does not exist
    result = await db.margins.update_many(
        {"is_visible": {"$exists": False}},
        {"$set": {"is_visible": True}}
    )
    print(f"Matched {result.matched_count} documents and modified {result.modified_count} documents.")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(migrate_margins())
