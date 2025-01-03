from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.modassembly.database.get_session import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(String, default="pending", nullable=False)
