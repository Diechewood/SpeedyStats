from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    UserID = Column(Integer, primary_key=True)
    Username = Column(String, unique=True, nullable=False)
    Email = Column(String, unique=True, nullable=False)
    PasswordHash = Column(String, nullable=False)
    DateCreated = Column(DateTime, default=datetime.utcnow)
    LastLogin = Column(DateTime, onupdate=datetime.utcnow)

class SpeedData(Base):
    __tablename__ = 'speed_data'

    SpeedDataID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey('users.UserID'), nullable=False)
    Speed = Column(Numeric, nullable=False)
    Timestamp = Column(DateTime, default=datetime.utcnow)
    Latitude = Column(Float)  # Storing latitude as a float
    Longitude = Column(Float) # Storing longitude as a float
    DeviceID = Column(String)  # Store device identifier if applicable

    user = relationship("User", back_populates="speed_data")

User.speed_data = relationship("SpeedData", order_by=SpeedData.SpeedDataID, back_populates="user")
