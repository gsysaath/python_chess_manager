from datetime import datetime
from pydantic import BaseModel
from typing import List
from pydantic.types import conint, constr

from models.match import Match
from orm.player_orm import players


class Turn(BaseModel):
    matches: List[Match] = []
    name: constr(min_length=7, max_length=10, strict=True)
    start_datetime: datetime = None
    end_datetime: datetime = None
    position: conint(strict=True, ge=1)

    def play(self):
        """ Play the turn """
        if self.end_datetime is None:
            for match in self.matches:
                match.play()
            self.end_datetime = datetime.now()

    def __str__(self):
        """ Depends if turn's matches are played or not """
        result = f"{self.name.title()}\n"
        result += f"Start time: {self.start_datetime.strftime('%m/%d/%Y, %H:%M:%S')}\n"
        if self.end_datetime:
            result += f"End time: {self.end_datetime.strftime('%m/%d/%Y, %H:%M:%S')}\n"
        for match in self.matches:
            player1 = players.find_by_id(match.player1_id)
            player2 = players.find_by_id(match.player2_id)
            if match.player1_score is not None:
                result += f"{player1.name} {match.player1_score.value} - {player2.name} {match.player2_score}\n"
            else:
                result += f"{player1.name} - {player2.name} - Not played yet \n"
        return result
