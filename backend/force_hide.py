import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def force_hide_has_altin():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("Forcing HAS ALTIN to Invisible...")
    result = await db.margins.update_one(
        {"product_name_key": "HAS ALTIN"},
        {"$set": {"is_visible": False}}
    )
    print(f"Modified count: {result.modified_count}")
    
    # Check result
    doc = await db.margins.find_one({"product_name_key": "HAS ALTIN"})
    print(f"New State -> {doc.get('product_name_key')}: {doc.get('is_visible')}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(force_hide_has_altin())
