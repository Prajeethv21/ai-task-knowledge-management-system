from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database.base import Base


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(80), nullable=False)
    details = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="activity_logs")
