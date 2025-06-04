from sqlalchemy import Column, Integer, String, Enum
from API.database import Base
import enum

class ProfileEnum(enum.Enum):
    admin = "admin"
    startup = "startup"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
    profile = Column(Enum(ProfileEnum), nullable=False)
    

class Startup(Base):
    __tablename__ = "startups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    incubator = Column(String(50), nullable=False) 
    stage = Column(String(50), nullable=False) 