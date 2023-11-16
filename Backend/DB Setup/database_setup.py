from sqlalchemy import create_engine
from models import Base
from database_config import DATABASE_URI
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    try:
        engine = create_engine(DATABASE_URI)
        Base.metadata.create_all(engine)
        logger.info("Database setup complete.")
    except SQLAlchemyError as e:
        logger.error(f"An error occurred during database setup: {e}")
        raise


if __name__ == "__main__":
    setup_database()
    print("Database setup complete.")
