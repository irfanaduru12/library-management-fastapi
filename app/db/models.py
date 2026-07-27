from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from app.db.database import Base
from sqlalchemy.orm import relationship

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = relationship("Author", back_populates="books")
    isbn = Column(String, nullable=True)
    is_borrowed = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=True) #nullable must be true in order to protect existing data
    page_number = Column(Integer, nullable=True)

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    books = relationship("Book", back_populates="author")
    birth_date = Column(Date, nullable=True)   

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True) 