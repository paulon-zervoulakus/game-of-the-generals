from fastapi import HTTPException
from typing import Callable
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from jose import jwt, JWTError, ExpiredSignatureError
from functools import wraps
from service_backend.settings import config_jwt
from service_backend.helpers.utils import templates

# def user_token_required(func: Callable):

#     @wraps(func)
#     async def wrapper(request: Request):
#         auth_token = request.cookies.get('access_token')
#         # Perform your validation logic here
#         if not auth_token:
#             raise HTTPException(status_code=401, detail="Token required")
        
#         try:
#             payload  = jwt.decode(
#                 auth_token, 
#                 config_jwt.SECRET_KEY, 
#                 algorithms=[config_jwt.ALGORITHM]
#             )
#         except JWTError as e:
#             raise HTTPException(status_code=401, detail="Invalid token")
        
#         except ExpiredSignatureError as e:
#             raise HTTPException(status_code=401, detail="Token expired")

#         except Exception as e:
#             raise HTTPException(status_code=500, detail="Internal server error")
        
#         return await func(request)

#     return wrapper

def user_token_required(func: Callable):

    @wraps(func)
    async def wrapper(request: Request, username: str = ""):
        auth_token = request.cookies.get('access_token')
        # Perform your validation logic here
        if not auth_token:
            return templates.TemplateResponse("error.html", status_code=401, context={"request": request, "error_code":"401 Missing Token", "message": "Authentication Required. Please login!"})
        
        try:
            payload = jwt.decode(
                auth_token, 
                config_jwt.SECRET_KEY, 
                algorithms=[config_jwt.ALGORITHM]
            )
            username: str = payload.get("sub")
        except ExpiredSignatureError as e:
            return templates.TemplateResponse("error.html", status_code=401, context={"request":request, "error_code":"401 Expired Token", "message": "Token Expired. Please re-login!"})
        
        except JWTError as e:
            return templates.TemplateResponse("error.html", status_code=401, context={"request":request, "error_code":"Token compromise", "message": "Invalid Token. Please login!"})
            
        except Exception as e:            
            return templates.TemplateResponse("error.html", status_code=500, context={"request":request, "error_code":"Server Error", "message": "Internal Server Error!"})
        
        return await func(request, username)

    return wrapper