from sqlalchemy import Integer, String, DateTime, Column, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer)
    telegram_name = Column(String)
    discord_id = Column(Integer)
    discord_name = Column(String)
    surname = Column(String)
    name = Column(String)
    subgroup = Column(Integer)

class Absence(Base):
    __tablename__ = 'absences'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime)
    text = Column(Text)