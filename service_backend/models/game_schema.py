import random
from enum import Enum
from pydantic import BaseModel
from typing import Dict

   
class GameFirstMove(Enum):
    creator = 1
    challenger = 2

class GameStatus(Enum):
    created = 1
    waiting_for_challenger = 2
    playing = 3
    finished = 4

Ranks = Enum('Ranks', [
    'FLAG', 'SPY', 'PRIVATE', 'SERGEANT', 
    'LIEUTENANT_2ND', 'LIEUTENANT_1ST', 'CAPTAIN', 
    'MAJOR', 'LIEUTENANT_COLONEL', 'COLONEL', 
    'STAR_GENERAL_1', 'STAR_GENERAL_2', 'STAR_GENERAL_3', 'STAR_GENERAL_4', 'STAR_GENERAL_5'])

class BattleResult(Enum):
    BOTH_LOSS = 0
    WIN = 1
    LOSS = 2
    
class Piece(BaseModel):
    def __init__(self, battle_result: BattleResult):
        self.battle_result = battle_result

    def battle(self, opponent_rank: str) -> BattleResult:        
        if opponent_rank == self.rank:
            return self.battle_result.BOTH_LOSS
        return self.battle_result.LOSS if opponent_rank in self.defeat_by else self.battle_result.WIN
       
class GeneralFiveStar(Piece):
    """5-Star General (5★): Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "5-Star General"
    rank = Ranks.STAR_GENERAL_5
    quantity = 1
    defeat_by = [Ranks.SPY]

class GeneralFourStar(Piece):
    """4-Star General (4★): Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "4-Star General"
    rank = Ranks.STAR_GENERAL_4
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5]

class GeneralThreeStar(Piece):
    """3-Star General (3★): Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "3-Star General"
    rank = Ranks.STAR_GENERAL_3
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4]

class GeneralTwoStar(Piece):
    """2-Star General (2★): Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "2-Star General"
    rank = Ranks.STAR_GENERAL_2
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3]

class GeneralOneStar(Piece):
    """1-Star General (1★): Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "1-Star General"
    rank = Ranks.STAR_GENERAL_1
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2]
    
class Colonel(Piece):
    """Colonel: Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "Colonel"
    rank = Ranks.COLONEL
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1]

class Lieutenant(Piece):
    """Lieutenant Colonel: Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "Lieutenant Colonel"
    rank = Ranks.LIEUTENANT_COLONEL
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL]

class Major(Piece):
    """Major: Can defeat all lower-ranked pieces except the Spy"""    
    __name__ = "Major"
    rank = Ranks.MAJOR
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL]

class Captain(Piece):
    """Captain: Can defeat all lower-ranked pieces except the Spy"""    
    __name__ = "Captain"
    rank = Ranks.CAPTAIN
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL, Ranks.MAJOR]

class FirstLieutenant(Piece):
    """1st Lieutenant: Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "1st Lieutenant"
    rank = Ranks.LIEUTENANT_1ST
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL, Ranks.MAJOR, Ranks.CAPTAIN]

class SecondLieutenant(Piece):
    """2nd Lieutenant: Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "2nd Lieutenant"
    rank = Ranks.LIEUTENANT_2ND
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL, Ranks.MAJOR, Ranks.CAPTAIN, Ranks.LIEUTENANT_1ST]

class Sergeant(Piece):
    """Sergeant: Can defeat all lower-ranked pieces except the Spy"""
    __name__ = "Sergeant"
    rank = Ranks.SERGEANT
    quantity = 1
    defeat_by = [Ranks.SPY, Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL, Ranks.MAJOR, Ranks.CAPTAIN, Ranks.LIEUTENANT_1ST, Ranks.LIEUTENANT_2ND]

class Private(Piece):
    """Private: Can defeat the Spy and the Flag."""
    __name__ = "Private"
    rank = Ranks.PRIVATE
    quantity = 6
    defeat_by = [Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL, Ranks.MAJOR, Ranks.CAPTAIN, Ranks.LIEUTENANT_1ST, Ranks.LIEUTENANT_2ND, Ranks.SERGEANT]

class Spy(Piece):
    """Spy: Can defeat the Private and the Flag. It is defeated by all higher-ranked pieces."""
    __name__ = "Spy"
    rank = Ranks.SPY
    quantity = 2
    defeat_by = [Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL, Ranks.MAJOR, Ranks.CAPTAIN, Ranks.LIEUTENANT_1ST, Ranks.LIEUTENANT_2ND, Ranks.SERGEANT]    

class Flag(Piece):
    """Flag: Cannot attack or defeat any other piece. It is captured when an opponent's piece lands on it."""
    __name__ = "Flag"
    rank = Ranks.FLAG
    quantity = 1
    defeat_by = [Ranks.STAR_GENERAL_5, Ranks.STAR_GENERAL_4, Ranks.STAR_GENERAL_3, Ranks.STAR_GENERAL_2, Ranks.STAR_GENERAL_1, Ranks.COLONEL, Ranks.LIEUTENANT_COLONEL, Ranks.MAJOR, Ranks.CAPTAIN, Ranks.LIEUTENANT_1ST, Ranks.LIEUTENANT_2ND, Ranks.SERGEANT, Ranks.SPY]    

game_pieces = {
    'FLAG' : { 'id' : 1, 'pos': '' },
    'SPY_1' : { 'id' : 2, 'pos': '' },
    'SPY_2' : { 'id' : 3, 'pos': '' },
    'PRIVATE_1' : { 'id' : 4, 'pos': '' },
    'PRIVATE_2' : { 'id' : 5, 'pos': '' },
    'PRIVATE_3' : { 'id' : 6, 'pos': '' },
    'PRIVATE_4' : { 'id' : 7, 'pos': '' },
    'PRIVATE_5' : { 'id' : 8, 'pos': '' },
    'PRIVATE_6' : { 'id' : 9, 'pos': '' },
    'SERGEAN' : { 'id' : 10, 'pos': '' },
    'SECOND_LIEUTENANT' : { 'id' : 11, 'pos': '' },
    'FIRST_LIEUTENANT' : { 'id' : 12, 'pos': '' },
    'CAPTAIN' : { 'id' : 13, 'pos': '' },
    'MAJOR' : { 'id' : 14, 'pos': '' },
    'LIEUTENANT_COLONEL' : { 'id' : 15, 'pos': '' },
    'COLONEL' : { 'id' : 16, 'pos': '' },
    'ONE_STAR_GENERAL' : { 'id' : 17, 'pos': '' },
    'TWO_STAR_GENERAL' : { 'id' : 18, 'pos': '' },
    'THREE_STAR_GENERAL' : { 'id' : 19, 'pos': '' },
    'FOUR_STAR_GENERAL' : { 'id' : 20, 'pos': '' },
    'FIVE_STAR_GENERAL' : { 'id' : 21, 'pos': '' }
}

class GameBoard(BaseModel):
    piece_dimension = 60
    board_map = [   ['A1','A2','A3','A4','A5','A6','A7','A8','A9'],
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
        }]
    
    def get_indices(coord):
        row = ord(coord[0]) - ord('A')
        col = int(coord[1]) - 1
        return row, col
 
    def randomize_position(self, gp: Dict[str, Dict[str, str]], creator: bool=True) -> Dict[str, Dict[str, str]]:
        
        x = self.spawning_slot[0]['player1' if creator else 'player2']
        positions = sum(x, [])
      
        # Iterate over the attributes of the GamePieces class
        for attribute_name, attribute_value in gp.items():
           
            # Get a random position from the list
            random_position = random.choice(positions)

            # Set the 'pos' value for the attribute
            attribute_value['pos'] = random_position

            # Remove the used position from the list to avoid repetition
            positions.remove(random_position)

        return gp