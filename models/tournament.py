from enum import Enum
from datetime import datetime
from typing import List

from pydantic import BaseModel, validator
from pydantic.types import PositiveInt, constr
from models.match import Match
from models.turn import Turn
from orm.player_orm import players

NAME_REGEX = r"^[A-Za-z -'éèï]{2,30}$"


class TimeControl(Enum):
    Bullet = 1
    Blitz = 2
    Rapid = 3


class Tournament(BaseModel):
    id: PositiveInt
    name: constr(regex=NAME_REGEX, strict=True)
    place: constr(regex=NAME_REGEX, strict=True)
    start_date: datetime = datetime.now()
    end_date: datetime = None
    number_of_turns: PositiveInt = 4
    time_control: TimeControl = TimeControl.Rapid
    description: constr(max_length=255, strict=True) = ""
    turns: List[Turn]
    players: List[PositiveInt]

    @validator('players')
    def players_must_be_even(cls, v):
        """ Validator, players number must be even """
        if len(v) % 2 != 0:
            raise ValueError('must be an even number')
        return v

    @validator('players')
    def players_list_must_be_greater_than_number_of_turns(cls, v, values):
        """ Validator, players must be greater than turns """
        if len(v) <= values["number_of_turns"]:
            raise ValueError("There must be more players than turns")
        return v

    def __init__(self, *args, **kwargs):
        """ Initialize tournament, then setup. """
        super().__init__(*args, **kwargs)
        self.setup()

    def __str__(self):
        return f"Name: {self.name}"

    @property
    def played_matches(self):
        res = []
        for turn in self.turns:
            for match in turn.matches:
                if match.played:
                    res.append(match)
        return res

    @property
    def matches(self):
        res = []
        for turn in self.turns:
            for match in turn.matches:
                res.append(match)
        return res

    def setup(self):
        """ Setup tournament first turn and its matches """
        if not self.matches:
            players_list = sorted([players.find_by_id(id) for id in self.players], key=lambda player: player.rank)
            first_turn = self.get_turn(pos=1)
            first_turn.start_datetime = datetime.now()
            first_turn.matches = [
                Match(player1_id=p1.id, player2_id=p2.id,)
                for p1, p2 in zip(players_list[:len(players_list)//2], players_list[len(players_list)//2:])
            ]

    def get_player_score(self, id: int):
        """ Returns a player score in this tournament """
        score = 0.0
        for turn in self.turns:
            for match in turn.matches:
                if match.get_player_score(id):
                    score += match.get_player_score(id)
        return score

    def setup_next_turn(self, turn_pos):
        """ Setup turn_pos turn with the Swiss tournament rules """
        turn = self.get_turn(turn_pos)
        if turn is not None and not turn.matches:
            players_list = sorted(
                [players.find_by_id(id) for id in self.players],
                key=lambda player: (-self.get_player_score(player.id), -player.rank)
            )
            while players_list:
                p1 = players_list.pop(0)
                for p2 in players_list:
                    m = Match(player1_id=p1.id, player2_id=p2.id)
                    if m not in self.matches:
                        turn.matches.append(m)
                        players_list.pop(players_list.index(p2))
                        break
                else:
                    p2 = players_list.pop(0)
                    m = Match(p1, p2)
                    turn.matches.append(m)
            turn.start_datetime = datetime.now()

    def get_turn(self, pos: int):
        """ Return the turn with position equal to parameter pos """
        for turn in self.turns:
            if pos == turn.position:
                return turn
        return None

    def play(self, orm):
        """ Plays the tournament """
        for pos, turn in enumerate(sorted(self.turns, key=lambda x: x.position), start=1):
            turn.play()
            self.setup_next_turn(pos+1)
            orm.save_item(self.id)
