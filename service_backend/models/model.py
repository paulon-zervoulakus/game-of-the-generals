from sqlalchemy import Column, Integer, String
from service_backend.models.databases import Base
from pydantic import BaseModel
from enum import Enum

class GameUsers(Base):
    __tablename__ = 'gameusers'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String) 
   

class BattleResult(Enum):
    BOTH_LOSS = 0
    WIN = 1
    LOSS = 2
    
class piece(BaseModel, BattleResult):
    def battle(self, opponent_rank: str) -> BattleResult:        
        if opponent_rank == self.rank:
            return self.BOTH_LOSS
        return self.LOSS if opponent_rank in self.defeat_by else self.WIN
            
        
class GeneralFiveStar(piece):
    """5-Star General (5★): Can defeat all lower-ranked pieces except the Spy and the Bomb."""
    __name__ = "5-Star General"
    rank = "5star"
    defeat_by =["spy","bomb"]

class GeneralFourStar(piece):
    """4-Star General (4★): Can defeat all lower-ranked pieces except the Spy and the Bomb."""
    __name__ = "4-Star General"
    id = "3star"
    defeat_by =["5star","spy","bomb"]

class GeneralThreeStar(piece):
    """3-Star General (3★): Can defeat all lower-ranked pieces except the Spy and the Bomb."""
    __name__ = "3-Star General"
    id = "3star"
    defeat_by =["5star","4star","spy","bomb"]

class GeneralTwoStar(piece):
    """2-Star General (2★): Can defeat all lower-ranked pieces except the Spy and the Bomb."""
    __name__ = "2-Star General"
    id = "2star"
    defeat_by =["5star","4star","3star","spy","bomb"]

class GeneralOneStar(piece):
    """1-Star General (1★): Can defeat all lower-ranked pieces except the Spy and the Bomb."""
    __name__ = "1-Star General"
    id = "1star"
    defeat_by =["5star","4star","3star","2star","spy","bomb"]


class Row(Enum):
    A=0
    B=1
    C=2
    D=3
    E=4
    F=5
    G=6
    H=7                                                                                                                                                                                                                                                                                                             
class GameBoard(BaseModel):
    piece_dimension = 60
    board = [['A1','A2','A3','A4','A5','A6','A7','A8','A9'],
             ['B1','B2','B3','B4','B5','B6','B7','B8','B9'],
             ['C1','C2','C3','C4','C5','C6','C7','C8','C9'],
             ['D1','D2','D3','D4','D5','D6','D7','D8','D9'],
             ['E1','E2','E3','E4','E5','E6','E7','E8','E9'],
             ['F1','F2','F3','F4','F5','F6','F7','F8','F9'],
             ['G1','G2','G3','G4','G5','G6','G7','G8','G9'],
             ['H1','H2','H3','H4','H5','H6','H7','H8','H9']]
    
