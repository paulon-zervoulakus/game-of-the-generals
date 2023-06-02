from pydantic import BaseModel

class GameUsersBase(BaseModel):
    id : int 
    username : str
    email : str

class GameUsersCreate(BaseModel):
    pass

class GameUsers(BaseModel):
    id : int

    class Config:
        orm_mode = True
