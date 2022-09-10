from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session


from .. import models,schemas,database,oauth2
from ..repository import crud

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
# models.Base.metadata.create_all(bind=engine)
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
get_db = database.get_db



router
@router.get("/", response_model=List[schemas.Post])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

@router.delete("/{post_id}/delete")
def delete_post(post_id:int,db:Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    return crud.delete_post(post_id, db)

@router.get("/{post_id}")
def read_post(post_id:int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    post = crud.get_post(db, post_id)
    return post

@router.put("/{post_id}",status_code = 202)
def edit_post(post_id, request:schemas.PostCreate, db:Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==post_id)
    if not post.first():
        raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
    post.update(request.dict())
    db.commit()
    return 'updated'
