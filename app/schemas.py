from pydantic import BaseModel,ConfigDict, EmailStr,Field
from datetime import datetime
from typing import Optional, Literal


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass




# RESPONSE MODEL vvv
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email:EmailStr
    created_at: datetime
# RESPONSE MODEL
class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

class PostOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    Post: Post
    votes : int 


# model for incomming user related requests 
# NOT A RESPONSE MODEL vvvv
class UserCreate(BaseModel):
    email:EmailStr
    password:str





# LOGIN REQUEST MODEL
class UserLogin(BaseModel):
    email:EmailStr
    password: str 


# Schema to validate when token is also sent by the user request 
class Token(BaseModel):
    access_token: str 
    token_type : str

# Schema to validate the payload structure inside the Token 
# But payload can be anything so id Field is set as Optional 
class TokenData(BaseModel):
    id: Optional[int] = None



class Vote(BaseModel):

    post_id: int 
    dir: Literal[0, 1]

