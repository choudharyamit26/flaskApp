from app.models import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import UTC, datetime


class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    founding_year = Column(Integer)
    website = Column(String(200))
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )

    # Relationships
    books = relationship("Book", back_populates="publisher")

    def __repr__(self):
        return f"<Publisher {self.name}>"
