from enum import Enum
from pydantic import BaseModel


Ranks = Enum('Ranks', [
    'FLAG', 'SPY', 'PRIVATE', 'SERGEANT', 
    'LIEUTENANT_2ND', 'LIEUTENANT_1ST', 'CAPTAIN', 
    'MAJOR', 'LIEUTENANT_COLONEL', 'COLONEL', 
    'STAR_GENERAL_1', 'STAR_GENERAL_2', 'STAR_GENERAL_3', 'STAR_GENERAL_4', 'STAR_GENERAL_5'])

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
    """5-Star General (5★): Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "5-Star General"
    rank = Ranks.STAR_GENERAL_5
    quantity = 1
    defeat_by = [Ranks.SPY]

class GeneralFourStar(piece):
    """4-Star General (4★): Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "4-Star General"
    rank = Ranks.STAR_GENERAL_4
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5]

class GeneralThreeStar(piece):
    """3-Star General (3★): Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "3-Star General"
    rank = Ranks.STAR_GENERAL_3
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4]

class GeneralTwoStar(piece):
    """2-Star General (2★): Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "2-Star General"
    rank = Ranks.STAR_GENERAL_2
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3]

class GeneralOneStar(piece):
    """1-Star General (1★): Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "1-Star General"
    rank = Ranks.STAR_GENERAL_1
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2]
    
class Colonel(piece):
    """Colonel: Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "Colonel"
    rank = Ranks.COLONEL
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1]

class Lieutenant(piece):
    """Lieutenant Colonel: Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "Lieutenant Colonel"
    rank = Ranks.LIEUTENANT_COLONEL
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL]

class Major(piece):
    """Major: Can defeat all lower-ranked pieces except the Spy"""    
    __name__ = "Major"
    rank = Ranks.MAJOR
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL]

class Captain(piece):
    """Captain: Can defeat all lower-ranked pieces except the Spy"""    
    __name__ = "Captain"
    rank = Ranks.CAPTAIN
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL, Ranks.MAJOR]

class FirstLieutenant(piece):
    """1st Lieutenant: Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "1st Lieutenant"
    rank = Ranks.LIEUTENANT_1ST
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL, Ranks.MAJOR, Ranks.CAPTAIN]

class SecondLieutenant(piece):
    """2nd Lieutenant: Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "2nd Lieutenant"
    rank = Ranks.LIEUTENANT_2ND
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL, Ranks.MAJOR, Ranks.CAPTAIN, Ranks.LIEUTENANT_1ST]

class Sergeant(piece):
    """Sergeant: Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "Sergeant"
    rank = Ranks.SERGEANT
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL, Ranks.MAJOR, Ranks.CAPTAIN, Ranks.LIEUTENANT_1ST, Ranks.LIEUTENANT_2ND]

class Private(piece):
    """Private: Can defeat the Spy and the Flag."""
    __name__ = "Private"
    rank = Ranks.PRIVATE
    quantity = 6
    defeat_by = [Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL, Ranks.MAJOR, Ranks.CAPTAIN, Ranks.LIEUTENANT_1ST, Ranks.LIEUTENANT_2ND, Ranks.SERGEANT]

class Spy(piece):
    """Spy: Can defeat the Private and the Flag. It is defeated by all higher-ranked pieces."""
    __name__ = "Spy"
    rank = Ranks.SPY
    quantity = 2
    defeat_by = [Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL, Ranks.MAJOR, Ranks.CAPTAIN, Ranks.LIEUTENANT_1ST, Ranks.LIEUTENANT_2ND, Ranks.SERGEANT]    

class Flag(piece):
    """Flag: Cannot attack or defeat any other piece. It is captured when an opponent's piece lands on it."""
    __name__ = "Flag"
    rank = Ranks.FLAG
    quantity = 1
    defeat_by = [Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL, Ranks.MAJOR, Ranks.CAPTAIN, Ranks.LIEUTENANT_1ST, Ranks.LIEUTENANT_2ND, Ranks.SERGEANT, Ranks.SPY]    


class GameBoard(BaseModel):
    piece_dimension = 60
    board = [   ['A1','A2','A3','A4','A5','A6','A7','A8','A9'],
                ['B1','B2','B3','B4','B5','B6','B7','B8','B9'],
                ['C1','C2','C3','C4','C5','C6','C7','C8','C9'],
                ['D1','D2','D3','D4','D5','D6','D7','D8','D9'],
                ['E1','E2','E3','E4','E5','E6','E7','E8','E9'],
                ['F1','F2','F3','F4','F5','F6','F7','F8','F9'],
                ['G1','G2','G3','G4','G5','G6','G7','G8','G9'],
                ['H1','H2','H3','H4','H5','H6','H7','H8','H9']]
       
    spawning_slot = [
        { 'player1' : [ ['A1','A2','A3','A4','A5','A6','A7','A8','A9'],
                ['B1','B2','B3','B4','B5','B6','B7','B8','B9'],
                ['C1','C2','C3','C4','C5','C6','C7','C8','C9']]
        },
        { 'player2' : [ ['F1','F2','F3','F4','F5','F6','F7','F8','F9'],
                ['G1','G2','G3','G4','G5','G6','G7','G8','G9'],
                ['H1','H2','H3','H4','H5','H6','H7','H8','H9']]    
        }
    ]
        
    def get_indices(coord):
        row = ord(coord[0]) - ord('A')
        col = int(coord[1]) - 1
        return row, col
    
    