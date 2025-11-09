from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app.database import Base

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String, unique=True)

    sent_messages = relationship(
        'Message',
        foreign_keys='Message.sender_id',  # Specify the foreign key for sent messages
        back_populates='sender'
    )

    # Relationship for messages received by the user
    received_messages = relationship(
        'Message',
        foreign_keys='Message.recipient_id',
        # Specify the foreign key for received messages
        back_populates='recipient'
    )


class Message(Base):
    __tablename__ = 'Messages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"))
    recipient_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"))
    content = Column(String)

    sender = relationship('User', foreign_keys=[sender_id],
                          back_populates='sent_messages', cascade="all, delete")
    recipient = relationship('User', foreign_keys=[recipient_id],
                             back_populates='received_messages',
                             cascade="all, delete")
