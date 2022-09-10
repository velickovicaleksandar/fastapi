from sqlalchemy.orm import Session

from giveaway_app import models, schemas, hashing


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()



def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hashing.Hash.bcrypt(user.password)
    db_user = models.User(email=user.email, username=user.username,password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()

def get_post(db: Session, post_id:int):
    return db.query(models.Post).filter(models.Post.id==post_id).first()

def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_item = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_post(id:int, db:Session):
    db.query(models.Post).filter(models.Post.id==id)\
        .delete(synchronize_session=False)
    db.commit()
    return 'deleted'

def edit_post(db: Session, post: schemas.Post, post_id: int):
    db.query(models.Post).filter(models.Post.id==post_id).update(post.dict())
    db.commit()
    return 'updated'



