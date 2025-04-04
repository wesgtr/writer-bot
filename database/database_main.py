from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route to create an article
@app.post("/articles/")
def create_article(user_id: int, title: str, content: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_article = models.Article(title=title, content=content, owner_id=user_id)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

# Route to get all articles by a specific user
@app.get("/users/{user_id}/articles/")
def get_user_articles(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.articles
