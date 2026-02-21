from fastapi import FastAPI,Response,status,HTTPException, Depends, APIRouter
from .. import models, schemas, utils 
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/users",
    tags = ['USERS']
)

#====================================================================================
# Endpoint for creating users and updating in user table

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate, db:Session = Depends(get_db)):

    #HASH THE PASSWORD - iseu.password
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    print(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user 

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int, db:Session = Depends(get_db)):

    user1 = db.query(models.User).filter(models.User.id == id).first()

    if not user1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} not found ")
    return user1
