import os
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from service_backend.settings import config_jwt
from service_backend.models.model import GameUsers

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../service_frontend/static")
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../service_frontend/templates")
templates = Jinja2Templates(directory=template_dir)

# class CsrfSettings(BaseModel):
#     secret_key:str = 'asecrettoeverybody'

# @CsrfProtect.load_config
# def get_csrf_config():
#     return CsrfSettings()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        config_jwt.SECRET_KEY, 
        algorithm=config_jwt.ALGORITHM
    )
    return encoded_jwt


###### Password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    return db.query(GameUsers).filter(GameUsers.username == username).first()

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_allowed_domains():
    domain_string = ','.join(map(str, config_jwt.ALLOWED_DOMAINS))
    return domain_string