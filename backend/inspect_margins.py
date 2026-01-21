import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

async def check_margins():
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("--- MARGINS COLLECTION ---")
    margins = await db.margins.find({}).to_list(1000)
    for m in margins:
        print(f"Product: {m.get('product_name_key')} | Visible: {m.get('is_visible')} | Percent: {m.get('is_percentage')}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_margins())
