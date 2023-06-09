import json
from datetime import timedelta, datetime
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from typing import Dict, Any
from sqlalchemy import desc
from sqlalchemy.orm import Session

from service_backend.models.databases import get_db 
from service_backend.models import model
from service_backend.models.game_schema import GameBoard, GameStatus, game_pieces
from service_backend.helpers.utils import templates, create_access_token
from service_backend.helpers.decorators import user_token_required
from service_backend.settings import config_jwt

router = APIRouter()

def get_last_spawning_position(username: str, db:Session=get_db()):
    last_game = db.query(model.GameRoomModel).filter(model.GameRoomModel.created_by == username).first()
    if last_game:

        return last_game.creator_spawn_position
    
    gb = GameBoard()
    return gb.randomize_position(gp=game_pieces, creator=True)


def create_game_data(data, db:Session=get_db()):
    user = db.query(model.UsersModel).filter(model.UsersModel.username == data['game_creator']).first()


    new_room = model.GameRoomModel(
        created_by = user.id,
        status = GameStatus.created,
        creator_spawn_position = json.dumps(data['spawning_position'])
    )
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room


@router.get('/', response_class=HTMLResponse)
@user_token_required
async def index(request: Request, username : str = ""):
    
    # initialize piece position base from the last game starting poing
    #   else randomize position or make default position
    data = {
        'game_creator': username,
        'spawning_position': get_last_spawning_position(username=username)
    }

    # create game data in database
    new_room = create_game_data(data)
    print(new_room)

    # create game token with database id
    access_token_expires = timedelta(minutes=config_jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
    game_room_token = create_access_token(
        {'game_id': new_room.id}, 
        expires_delta=access_token_expires
    )

    print(game_room_token)

    # initialize socket room with auth credentials

    # publish the room in lobby so everyone else can see and join

    # player can only see the pieces that they own
    # player's opponent will be covered to hide the identity of the pieces. only the position is reveled 
    
    # game creator will choose who will move first
    # both player must thick the status ready to battle, and countdown will emense before the battle bagan

    # expectators cannot see players pieces identity. only the position.
    # expectators will see the lossing piece after a collission of pieces happens

    # everybody in the room can participate in the chat

    context = {
        'request': request,
        'status': 'game created',
        'username': username
    }
    return templates.TemplateResponse("room.html", context)
