# DataProcessingService.py
from pymongo import MongoClient
from DatabaseConfig import MongoDBConfig
import statistics

class DataProcessingService:
    def __init__(self):
        self.client = MongoClient(f"mongodb://{MongoDBConfig.USER}:{MongoDBConfig.PASSWORD}@{MongoDBConfig.HOST}:{MongoDBConfig.PORT}")
        self.db = self.client[MongoDBConfig.DATABASE]
        self.raw_data_collection = self.db['raw_speed_data']
        self.processed_data_collection = self.db['processed_speed_data']

    def process_user_data(self, user_id):
        try:
            user_data = list(self.raw_data_collection.find({"user_id": user_id}))
            speeds = [data['speed'] for data in user_data]
            average_speed = statistics.mean(speeds)
            max_speed = max(speeds)

            self.processed_data_collection.insert_one({
                "user_id": user_id,
                "average_speed": average_speed,
                "max_speed": max_speed
            })
            return True
        except Exception as e:
            print(f"Error processing data: {e}")
            return False

    def __del__(self):
        self.client.close()

