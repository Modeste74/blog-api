from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session, joinedload
from db_setup import Base, engine, get_db, User, Post, Comment
from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime, timedelta

# Initialize FastAPI app
app = FastAPI()

# Create all tables
Base.metadata.create_all(bind=engine)

# Security setup
SECRET_KEY = "f4a9b6e3c6d8437d9f3a9e1b8a2f4c6d0e3b1a9d8c7e5f2b3d1c4a9f6e7b8d2c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# === Pydantic Schemas ===
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class PostCreate(BaseModel):
    title: str
    content: str

class CommentCreate(BaseModel):
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    post_author: str

    class Config:
        orm_mode = True

class PostsResponse(BaseModel):
    posts: List[PostResponse]

# Helper to hash passwords
def hash_password(password):
    return pwd_context.hash(password)

# Verify password
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# Generate JWT token
def create_access_token(data: dict, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Decode token & get user
def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise credentials_exception
    return user

# Routes

# Register a new user
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hash_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password=hash_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created", "user": new_user.username}

# Login
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
                status_code=401,
                detail="Invalid credentials")
    token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": token, "token_type": "bearer"}


# Create a post (auth required)
@app.post("/posts")
def create_post(
        post: PostCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    new_post = Post(
            title=post.title,
            content=post.content,
            user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"msg": "Post created", "post": new_post.title}

# Getting all posts
@app.get("/posts", response_model=PostsResponse)
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).options(joinedload(Post.user)).all()
    if not posts:
        raise HTTPException(status_code=404, detail="No posts present")
    return {
        "posts": [
            PostResponse(
                id=p.id,
                title=p.title,
                content=p.content,
                post_author=p.user.username
            )
            for p in posts
        ]
    }


# Delete own post (auth + ownership required)
@app.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    post = db.query(Post).filter(Post.id == post_id, Post.user_id == current_user.id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not yours")
    
    db.delete(post)
    db.commit()
    return {"msg": "Post deleted"}

# Adding comments on post
@app.post("/posts/{post_id}/comments")
def add_comment(
        post_id: int,
        comment: CommentCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    new_comment = Comment(
            content=comment.content,
            user_id=current_user.id,
            post_id=post_id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {
        "msg": "Comment added",
        "comment": new_comment.content,
        "post": post.title,
        "by": current_user
    }

# Getting all the comments under a post
@app.get("/posts/{post_id}/comments")
def get_comments(
    post_id: int,
    db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return {
        "post": post.title,
        "comments": [
            {
                "id": c.id,
                "content": c.content,
                "user": c.user.username
            } for c in comments
        ]
    }

# Delete your own comments
@app.delete("/comments/{comment_id}")
def delete_content(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    comment = db.query(Comment).filter(Comment.id == comment_id, Comment.user_id == current_user.id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found or not yours")
    
    db.delete(comment)
    db.commit()
    return {"msg": "Comment deleted"}
