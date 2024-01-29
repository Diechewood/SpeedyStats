# DataProcessingService.py
import asyncpg
from DatabaseConfig import PostgreSQLConfig
import statistics

class DataProcessingService:
    async def connect(self):
        self.connection = await asyncpg.connect(
            user=PostgreSQLConfig.USER,
            password=PostgreSQLConfig.PASSWORD,
            database=PostgreSQLConfig.DATABASE,
            host=PostgreSQLConfig.HOST
        )

    async def process_user_data(self, user_id):
        try:
            # Connect to the database
            await self.connect()

            # Fetch raw speed data for the user
            raw_data = await self.connection.fetch("SELECT speed FROM speed_data WHERE user_id = $1", user_id)
            speeds = [data['speed'] for data in raw_data]
            
            # Calculate metrics
            average_speed = statistics.mean(speeds) if speeds else 0
            max_speed = max(speeds) if speeds else 0

            # Processed data logic here

            return True
        except Exception as e:
            print(f"Error processing data: {e}")
            return False
        finally:
            await self.connection.close()
