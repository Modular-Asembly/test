from sqlalchemy import Column, Integer, String
from app.modassembly.database.get_session import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    quantity = Column(Integer, default=0, nullable=False)
