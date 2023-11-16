from sqlalchemy import create_engine
from models import Base
from database_config import DATABASE_URI
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    setup_database()
    print("Database setup complete.")
