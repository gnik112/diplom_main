from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
#from sqlalchemy.orm import relationship


class Room(Base):
    __tablename__ = 'room'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    people_count = Column(Integer)
    cost = Column(Float)

