from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
#from sqlalchemy.orm import relationship


class Booking(Base):
    __tablename__ = 'booking'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    room_id = Column(Integer, ForeignKey("room.id"), nullable=False, index=True)
    date = Column(Date)
    beg_hour = Column(Integer)
    beg_min = Column(Integer)
    end_hour = Column(Integer)
    end_min = Column(Integer)
    confirm = Column(Boolean)
