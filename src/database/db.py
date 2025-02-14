import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

client = None
db = None
load_dotenv()

async def connect_to_mongo():
    global client, db
    client = AsyncIOMotorClient(os.getenv('DATABASE_URL'))
    db = client['chatbot-processes-prod']
    print("Connected to MongoDB")


async def close_mongo_connection():
    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")