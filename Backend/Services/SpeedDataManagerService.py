# SpeedDataManagerService.py
from pymongo import MongoClient
from DatabaseConfig import MongoDBConfig

class SpeedDataManagerService:
    def __init__(self):
        self.client = MongoClient(f"mongodb://{MongoDBConfig.USER}:{MongoDBConfig.PASSWORD}@{MongoDBConfig.HOST}:{MongoDBConfig.PORT}")
        self.db = self.client[MongoDBConfig.DATABASE]
        self.collection = self.db['raw_speed_data']

    def record_speed_data(self, user_id, speed, timestamp, location):
        try:
            self.collection.insert_one({
                "user_id": user_id,
                "speed": speed,
                "timestamp": timestamp,
                "location": location
            })
            return True
        except Exception as e:
            print(f"Error recording speed data: {e}")
            return False

    def __del__(self):
        self.client.close()
