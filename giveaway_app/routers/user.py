from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session


from .. import schemas,database,oauth2
from ..repository import crud

# from ..database import SessionLocal, engine
router = APIRouter(
    prefix="/users",
    tags=['User']
)
# models.Base.metadata.create_all(bind=engine)
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
get_db = database.get_db

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/{user_id}/posts/", response_model=schemas.Post)
def create_item_for_user(
    user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return crud.create_user_post(db=db, post=post, user_id=user_id)









