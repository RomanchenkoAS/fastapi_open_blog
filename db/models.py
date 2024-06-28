from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

from db.database_definition import Base

# Define the naming conventions
naming_convention = {
    "ix": "ix_%(column_0_label)s",  # Index
    "uq": "uq_%(table_name)s_%(column_0_name)s",  # Unique constraint
    "ck": "ck_%(table_name)s_%(constraint_name)s",  # Check constraint
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # Foreign key
    "pk": "pk_%(table_name)s",  # Primary key
    "table": "%(model_name)s_t",  # Table name pattern
}


def timestamp() -> datetime:
    return datetime.now(timezone.utc)


class DbBlogPost(Base):
    __tablename__ = "blog_posts_t"
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    content = Column(String, nullable=True)
    image = Column(LargeBinary, nullable=True)
    date_posted = Column(DateTime, default=timestamp)
    date_updated = Column(DateTime, default=timestamp, onupdate=timestamp)

    # Foreign
    author_id = Column(Integer, ForeignKey("authors_t.id"), nullable=False)
    author = relationship("DbAuthor", back_populates="posts")

    def __repr__(self):
        return f"<BlogPost {self.id} '{self.title}'>"


class DbAuthor(Base):
    __tablename__ = "authors_t"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    last_posted = Column(DateTime, default=timestamp, nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)

    # Foreign
    posts = relationship("DbBlogPost", back_populates="author")

    def __repr__(self):
        return f"<Author {self.id} {self.name}>"
