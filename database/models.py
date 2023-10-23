from sqlalchemy import Integer, String, DateTime, Column
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer)
    telegram_name = Column(String)
    surname = Column(String)
    name = Column(String)
    subgroup = Column(Integer)