from app.modassembly.database.get_session import Base

from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    role = Column(String, index=True, default="user", nullable=False)
