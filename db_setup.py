from sqlalchemy import create_engine, Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
# from sqlalchemy.exc import IntegrityError

# Create our Database
DATABASE_URL = "sqlite:///blog.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # sqlite specific
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency for fastapi to get DB session
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Defining Models
# User Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)

    # Relationships to posts
    posts = relationship('Post', back_populates='user', cascade="all, delete-orphan")
    comments = relationship('Comment', back_populates='user', cascade="all, delete-orphan")
    


# Post Model
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    user = relationship('User', back_populates='posts')
    comments = relationship("Comment", back_populates="post")

# Comment Model
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    # Relationships
    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')
