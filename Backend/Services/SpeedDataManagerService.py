# SpeedDataManagerService.py
from motor.motor_asyncio import AsyncIOMotorClient
from DatabaseConfig import MongoDBConfig
import asyncio

class SpeedDataManagerService:
    def __init__(self):
        self.client = AsyncIOMotorClient(f"mongodb://{MongoDBConfig.USER}:{MongoDBConfig.PASSWORD}@{MongoDBConfig.HOST}:{MongoDBConfig.PORT}")
        self.db = self.client[MongoDBConfig.DATABASE]
        self.collection = self.db['raw_speed_data']

    async def record_speed_data(self, user_id, speed, timestamp, location):
        try:
            await self.collection.insert_one({
                "user_id": user_id,
                "speed": speed,
                "timestamp": timestamp,
                "location": location
            })
            return True
        except Exception as e:
            print(f"Error recording speed data: {e}")
            return False
