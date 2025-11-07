from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database import Base

class Message(Base):
    __tablename__ = 'Messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender = Column(Integer, ForeignKey("users.id"))
    recipient = Column(Integer, ForeignKey("users.id"))
    content = Column(String)

    users = relationship("Users", back_populates="message", cascade="all, delete")