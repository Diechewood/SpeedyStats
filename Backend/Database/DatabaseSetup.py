# DatabaseSetup.py
import psycopg2
from pymongo import MongoClient
from DatabaseConfig import PostgreSQLConfig, MongoDBConfig

# PostgreSQL setup
def setup_postgresql():
    try:
        # Connect to PostgreSQL
        connection = psycopg2.connect(
            database=PostgreSQLConfig.DATABASE,
            user=PostgreSQLConfig.USER,
            password=PostgreSQLConfig.PASSWORD,
            host=PostgreSQLConfig.HOST,
            port=PostgreSQLConfig.PORT
        )
        cursor = connection.cursor()

        # Create tables for users and speed data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS speed_data (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                timestamp TIMESTAMP NOT NULL,
                speed DECIMAL NOT NULL,
                location GEOGRAPHY(Point, 4326)
            );
        """)

        connection.commit()
        print("PostgreSQL setup completed successfully.")
    except Exception as error:
        print(f"Error setting up PostgreSQL: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# MongoDB setup
def setup_mongodb():
    try:
        # Connect to MongoDB
        client = MongoClient(f"mongodb://{MongoDBConfig.USER}:{MongoDBConfig.PASSWORD}@{MongoDBConfig.HOST}:{MongoDBConfig.PORT}")
        db = client[MongoDBConfig.DATABASE]

        # Create collections for raw and processed speed data
        db.create_collection('raw_speed_data')
        db.create_collection('processed_speed_data')

        print("MongoDB setup completed successfully.")
    except Exception as error:
        print(f"Error setting up MongoDB: {error}")

def main():
    setup_postgresql()
    setup_mongodb()

if __name__ == "__main__":
    main()

