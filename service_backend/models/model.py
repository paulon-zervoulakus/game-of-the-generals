from sqlalchemy import Column, Integer, String
from service_backend.models.databases import Base

class GameUsers(Base):
    __tablename__ = 'gameusers'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String) 
   
