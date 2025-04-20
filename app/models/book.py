from app.models import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Numeric,
    Text,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import UTC, datetime


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    isbn = Column(String(13), unique=True)
    publication_date = Column(Date)
    price = Column(Numeric(10, 2))
    description = Column(Text)

    # Foreign keys
    author_id = Column(
        Integer, ForeignKey("authors.id", ondelete="SET NULL"), nullable=True
    )
    publisher_id = Column(
        Integer, ForeignKey("publishers.id", ondelete="SET NULL"), nullable=True
    )

    # Relationships
    author = relationship("Author", back_populates="books")
    publisher = relationship("Publisher", back_populates="books")

    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(
        DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )

    def __repr__(self):
        return f"Book {self.title}"
