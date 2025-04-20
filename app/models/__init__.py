from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.user import User
from app.models.author import Author
from app.models.book import Book
from app.models.publisher import Publisher
