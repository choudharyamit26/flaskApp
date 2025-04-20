from app.models import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import UTC, datetime


class Insight(Base):
    __tablename__ = "insight"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))
    book_id = Column(
        Integer, ForeignKey("books.id", ondelete="SET NULL"), nullable=True
    )
    book = relationship("Book", back_populates="insights")

    def __repr__(self):
        return f"Insight {self.title}"
