from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
#from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    access_token = Column(String)
