import re
import json 
# from urllib.parse import urlencode
from datetime import timedelta, datetime
from typing import  Union, List
from pydantic import BaseModel, validator, ValidationError

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response
from fastapi.requests import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from service_backend.settings import config_jwt
from service_backend.models.model import GameUsers
from service_backend.models.databases import get_db
from service_backend.models.schema import GameUsersBase
from service_backend.helpers.utils import templates, get_password_hash, authenticate_user, create_access_token, get_allowed_domains

router = APIRouter()

class ResponseData(BaseModel):
    message : str
    data : Union[List[GameUsersBase], None] 

@router.post("/login/")
async def login_for_access_token(
    request: Request,
    db: Session = Depends(get_db)):
    
    data = await request.json()
    
    user = authenticate_user(db, data['username'], data['password'])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config_jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
   
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    response = Response(status_code=200, content=json.dumps({"message":"Login successful","username":data['username']}))

    expiration_datetime = datetime.now() + access_token_expires
    expires = expiration_datetime.strftime("%a, %d %b %Y %H:%M:%S GMT")
    allowed_domains = ','.join(map(str, config_jwt.ALLOWED_DOMAINS))
    response.set_cookie(
        "access_token", access_token, 
        httponly=True, 
        expires=expires,
        domain=allowed_domains)

    return response

@router.get("/login/")
def form(request: Request):
    response = templates.TemplateResponse('account/flogin-form.html', { 'request': request })     
    return response  

@router.get("/create-user/")
def form_create_user(request: Request):
    response = templates.TemplateResponse('account/fcreate-form.html', { 'request': request })     
    return response  


def is_valid_email(email: str) -> bool:
    # Regular expression pattern for email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

class CreateForm(BaseModel):
    username: str
    password: str
    password2: str
    email: str

    @validator('username')
    def check_username_length(cls, username):
        if len(username) <= 2:
            raise ValueError("Username needs 3 or more characters in length")
        return username
    
    @validator('password')
    def check_password_length(cls, password):
        if len(password) <= 3:
            raise ValueError("Password needs 4 or more characters in length")
        return password

    @validator('password2')
    def passwords_match(cls, password2, values, **kwargs):
        if 'password' in values and password2 != values['password']:
            raise ValueError("Passwords do not match")
        return password2    

    @validator('email')
    def check_email(cls, email):
        if not is_valid_email(email):
            raise ValueError("Invalid Email Format")
        return email
    
    def get_password(self):
        return get_password_hash(self.password)
    
@router.post("/create-user/")
async def form_save_user(
    request: Request,
    db: Session = Depends(get_db)):
    data = await request.json()
    
    
    try:       
        form = CreateForm(
            username=data['username'],
            password=data['password'],
            password2=data['password2'],
            email=data['email']
        )

        new_user = GameUsers(
            username=form.username,
            hashed_password=form.get_password(),
            email=form.email
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return JSONResponse(status_code=200, content={"message":"Successfully created a User"})
     
    except ValidationError as e:       

        error_messages = {}
        for error in e.errors():
            field = error['loc'][0]
            message = error['msg']
            error_messages[field] = message
                
    except IntegrityError as e:
        db.rollback()  # Rollback the transaction
        # Handle the exception here, such as logging the error or returning an error response
       
        error_messages = {
            'username':'Username already taken or used',
            'email':'Email already exists'
        }

    submitted_data = {
        'username':data['username'],
        'email':data['email'],
        'error':error_messages
    }
    return JSONResponse(status_code=400, content=submitted_data) 
