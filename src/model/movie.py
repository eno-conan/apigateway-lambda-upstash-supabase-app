from sqlalchemy import Boolean, Column, Integer, String

from src.database import Base


class User(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=False, index=True)
    description = Column(String, unique=True)
