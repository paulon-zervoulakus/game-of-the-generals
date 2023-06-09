import json
import asyncio
from datetime import timedelta, datetime
from fastapi import APIRouter, status, Query
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response

from pydantic import ValidationError
from typing import Annotated, Dict, Any
from jose import jwt, JWTError, ExpiredSignatureError

from service_backend.settings import config_jwt
from service_backend.helpers.utils import create_access_token
from service_backend.helpers.decorators import user_token_required

router = APIRouter()

@router.get("/ping-session-status/{sleep_time}/")
async def ping_from_client(
    request: Request,
    sleep_time: int = Annotated[int, Query(ge=1)]):
    
    await asyncio.sleep(int(sleep_time))
    auth_token = request.cookies.get('access_token')    
    if auth_token:   
        try:     
            payload  = jwt.decode(
                auth_token, 
                config_jwt.SECRET_KEY, 
                algorithms=[config_jwt.ALGORITHM],
                options={"verify_exp":True}
            )
            username: str = payload.get("sub")
            if username:
                response = JSONResponse(status_code=200, content={"message":"Authenticated","username":username, "session_status":True})
            else:
                response = JSONResponse(status_code=200, content={"message":"Invalid Token", "session_status":False})
                
        except (JWTError, ValidationError, ExpiredSignatureError) as e:                        
            response = JSONResponse(status_code=200, content={"session_status":False})
        
    else:        
        print("ping session status auth_token null >>>>>")
        response = JSONResponse(status_code=200, content={"session_status":False})
        
    return response


@router.get("/logout/")
async def logout( 
    request: Request,
    response: Response ):    
    try:     
        auth_token = request.cookies.get('access_token')
        if auth_token:
            payload  = jwt.decode(auth_token, config_jwt.SECRET_KEY, algorithms=[config_jwt.ALGORITHM])
            username: str = payload.get("sub")

            # for x in config_jwt.ALLOWED_DOMAINS:
            response = Response(status_code=200, content=json.dumps({"message":"Logout successful","username":username}))

            access_token_expires = timedelta(minutes=config_jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
   
            access_token = create_access_token(
                data={"invalidate_access": username}, 
                expires_delta=access_token_expires
            )
            expiration_datetime = datetime.now() - access_token_expires
            expires = expiration_datetime.strftime("%a, %d %b %Y %H:%M:%S GMT")

            allowed_domains = ','.join(map(str, config_jwt.ALLOWED_DOMAINS))
            response.set_cookie(
                "access_token", access_token,
                domain=allowed_domains,
                httponly=True, 
                expires=expires)

            response = response
    except (JWTError, ValidationError):
        response =  JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message":"Logout Error","error":"INVALID_TOKEN"})
        

    return response
    
@router.get("/get-user-token/")
async def get_user_token(
    request: Request
):
    
    try:
        auth_token = request.cookies.get('access_token')
    except JWTError:
        auth_token = False
        
    if auth_token:
       
        payload  = jwt.decode(
            auth_token, 
            config_jwt.SECRET_KEY, 
            algorithms=[config_jwt.ALGORITHM]
        )
        username: str = payload.get("sub")

        access_token_expires = timedelta(minutes=config_jwt.ACCESS_TOKEN_EXPIRE_MINUTES)


        game_access_token = create_access_token(
            data={"username": username}, 
            expires_delta=access_token_expires
        )
        
        # Convert the expiration datetime to the required format
        # expires = access_token_expires.strftime("%a, %d %b %Y %H:%M:%S GMT")

        return JSONResponse(status_code=200, content={"message":"game access","game_user_token":game_access_token, "session_status":True})

       

    return JSONResponse(status_code=401, content={"messaage":"Unauthorized Access","session_status":False})



@router.get("/create-game/")
@user_token_required
async def create_game(request: Request, payload: Dict[str, Any]):
    print(payload)
  
    return JSONResponse(status_code=200, context={"request":request, "message":"Hello"})