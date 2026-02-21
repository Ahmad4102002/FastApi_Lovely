from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils ,oauth2




router = APIRouter(tags= ['Authentication'])

@router.post('/login', response_model=schemas.Token)    # vvv user_credentials.username , user_credentials.password
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    

    #username ,password OAuth
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() # CONTAIN ACTUAL USERNAME AND PASSWORD HASH RETREIVED FORM THE DB 

    # IF USER IS NULL THEN (INVALID CREDENTIALS)
    if not user:

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= "Invalid Credentials")
    
    # UTILS.VERIFY takes two passwords. First password is from the api request and the secoend is from the DB Response (HASHED).
    # So the utils.verify converts the api request password to its hashed format and then check if they ar e same or not

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Invalid Credentials")
    
    # Create token
    # Return token                            # dict to be sent for payload encoding
    access_token = oauth2.create_access_token(data = {"user_id": user.id}) # id here refers to the id of the user (Probably used to track login sessions later MAYBE)

    return {"access_token": access_token, "token_type": "bearer"} # I Think the front end will be responsible to trace the access token to the current user so  
                                                                  # the user dosent have to each time copy and paste tokens to authenticate after login