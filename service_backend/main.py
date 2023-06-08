
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from service_backend.helpers.utils import static_dir
from service_backend.routes.lobby import router as lobby_router
from service_backend.routes.account import router as account_router
from service_backend.routes.room import router as room_router
from service_backend.routes.api import router as api_router
# from service_backend.models.databases import engine
# from service_backend.models.model import Base
from service_backend.settings import config_global

# Base.metadata.create_all(bind=engine)
 
app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir), name="static")

## CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(lobby_router, prefix="")
app.include_router(account_router, prefix="/account")
app.include_router(api_router, prefix='/api')
app.include_router(room_router, prefix='/room')


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config_global.HOST,
        port=int(config_global.PORT),
        reload=True        
    )