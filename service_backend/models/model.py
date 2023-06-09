from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, func

from service_backend.models.game_schema import GameFirstMove, GameStatus

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UsersModel(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String) 
    date_created = Column(DateTime, default=func.now())
   

class GameRoomModel(Base):
    __tablename__ = 'gameroom'

    id = Column(Integer, primary_key=True, index=True)
    first_move = Column(Integer, default=GameFirstMove.creator)    
    date_created = Column(DateTime, default=func.now())
    created_by = Column(Integer, ForeignKey('user.id'))
    challenger = Column(Integer, ForeignKey('user.id'))
    status = Column(Integer, default=GameStatus.created)
    creator_spawn_position = Column(String)
    challenger_spaw_position = Column(String)
    

class GameRecordModel(Base):
    __tablename__ = 'gamerecord'
    id = Column(Integer, primary_key=True, index=True) 
    game_room = Column(Integer, ForeignKey('gameroom.id'))
    move_by = Column(Integer, ForeignKey('user.id'))
    # move_time = timer 
    # move_duel = [move,win,lose]
    # owner_piece_id:from:to:challenger_piece_id:move_duel
    piece_move = Column(String)
