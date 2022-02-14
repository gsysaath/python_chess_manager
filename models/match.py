from enum import Enum

from pydantic import BaseModel
from pydantic.types import PositiveInt

from views.menu_view import PickWinnerMenu
from orm.player_orm import players


class Score(Enum):
    Win = 1.0
    Lose = 0.0
    Draw = 0.5


class Match(BaseModel):
    player1_id: PositiveInt
    player2_id: PositiveInt
    player1_score: Score = None

    @property
    def player2_score(self):
        """ Returns player2 score """
        return 1.0 - self.player1_score.value if self.player1_score is not None else None

    @player2_score.setter
    def player2_score(self, value):
        """ Setter player2 score """
        self.player1_score = 1.0 - value

    @property
    def played(self):
        """ Returns if the match has been played """
        return self.player1_score is not None

    def get_player_score(self, id: int):
        """ Returns player with id=id score, None if the match hasnt been played yet """
        match id:
            case self.player1_id:
                return self.player1_score.value
            case self.player2_id:
                return self.player2_score
            case _:
                return None

    def __eq__(self, obj):
        """ Returns if two matches are equal, (a,b) == (b,a) """
        if not isinstance(obj, Match):
            raise "Not comparable"
        else:
            return min(obj.player1_id, obj.player2_id) == min(self.player1_id, self.player2_id) and \
                max(obj.player1_id, obj.player2_id) == max(self.player1_id, self.player2_id)

    def play(self):
        """ Play the match  """
        if not self.played:
            player1 = players.find_by_id(self.player1_id)
            player2 = players.find_by_id(self.player2_id)
            self.player1_score = Score(PickWinnerMenu(player1.name, player2.name).exec())

    def __str__(self):
        """ Returns player1 name player2 name and result"""
        player1 = players.find_by_id(self.player1_id)
        player2 = players.find_by_id(self.player2_id)
        if self.player1_score is not None:
            return f"{player1.name} {self.player1_score.value} - {player2.name} {self.player2_score}"
        else:
            return f"{player1.name} - {player2.name} - Not played yet"
