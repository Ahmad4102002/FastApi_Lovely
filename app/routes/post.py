from fastapi import FastAPI,Response,status,HTTPException, Depends, APIRouter
from .. import models, schemas ,oauth2
from ..database import get_db
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['POSTS']
)

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit:int = 10, skip: int = 0, search : Optional[str] = ""):
        # RAW SQL 
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # DATABASE SESSION ---query----SESSION CLOSE

    # RESPONSE MODEL IS CALLED: here response model must be called multiple times as \
    # the variable posts contains multiple entries fetched from the database.
    # So response model is assigned a list   
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id ==models.Post.id,
                                         isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results

#-------------------- ADD POSTS --------------------------------

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):

        # RAW SQL 
    #cursor.execute("""INSERT INTO posts (content, published, rating, title) VALUES (%s,%s,%s,%s) RETURNING * """,
    #               (post.content,post.published,post.rating,post.title,))
    #posts = cursor.fetchone()
    #conn.commit()

    new_post  = models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#------------------------GET POST BY ID ---------------------------------------

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int, db:Session  = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):
    
        #RAW SQL
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""",str(id))
    #post = cursor.fetchone()

    post =  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id ==models.Post.id,
                                         isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} : id not found")
    return post

#---------------------------DELETE BY ID --------------------------------------

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{id} : id not found"
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= "Not Authorized to Perform this")

    post_query.delete(synchronize_session=False)
    db.commit()

    return {"delete" : "success"}
#-------------------------UPDATE BY ID-------------------------------------------
    
@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post:schemas.PostCreate, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):

    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s RETURNING * """,
    #               (post.title,post.content,post.published,post.rating,str(id),))
    #conn.commit()
    #updated_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id) 

    post_1 = post_query.first()

    if post_1 is None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"{id} : id not found" )
    
    if post_1.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= "Not Authorized to Perform this")
    
    post_query.update(post.model_dump(), synchronize_session=False)
    
    db.commit()

    return post_query.first()