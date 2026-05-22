from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.database.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_name = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    size = Column(Integer, nullable=False)
    chunk_count = Column(Integer, nullable=False, default=0)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime, server_default=func.now())

    uploader = relationship("User", back_populates="documents_uploaded")
