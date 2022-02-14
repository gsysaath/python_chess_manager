from typing import Any, List, Tuple
from enum import Enum


from views.view import View


class Menu(View):
    def __init__(self, title: str, choices: List[Tuple[str, Any]]):
        self.choices = choices
        content = '\n'.join(
            [f'{i} - {choice}' for i, (choice, _) in enumerate(choices, start=1)])
        super().__init__(title=title, content=content)

    def exec(self):
        while True:
            try:
                super().exec()
                choice = int(input("What would you like to do? : "))
                if choice < 1 or choice > len(self.choices):
                    raise ValueError
                return self.choices[choice - 1][1]
            except ValueError as e:
                print(e)
                pass


class EnumMenu(Menu):
    """ Allows you to choose within an Enum list """
    def __init__(self, title: str, enum: Enum):
        super().__init__(title=title, choices=[(e.name, e) for e in enum])


class HomeMenu(Menu):
    def __init__(self):
        """ Home Menu """
        super().__init__(title="Home Menu", choices=[
            ("Players", '/players'),
            ("Tournaments", '/tournaments'),
            ("Quit", '',)
        ])


class PlayerMenu(Menu):
    def __init__(self):
        """ Player Menu"""
        super().__init__(title="Player Menu", choices=[
            ("Add a new player", "/players/add"),
            ("List of players ordered by last name", "/players/all/sort-by-name"),
            ("List of players ordered by rank", "/players/all/sort-by-rank"),
            ("Previous menu", "/"),
        ])


class TournamentMenu(Menu):
    def __init__(self):
        """ Tournament Menu"""
        super().__init__(title="Tournament Menu", choices=[
            ("Create a new tournament", "/tournaments/add"),
            ("List of all tournaments", "/tournaments/all"),
            ("More details about one tournament", "/tournaments/info"),
            ("Previous menu", "/")
        ])


class SelectItemMenu(Menu):
    def __init__(self, items: List[Any]):
        """ Select Item Menu """
        super().__init__(title="Select choice", choices=[
            (str(item), item.id) for item in items
        ])
        self.items = items

    def exec(self):
        choice = super().exec()
        self = self.__init__(items=[item for item in self.items if item.id != choice])
        return choice


class TournamentShowMenu(Menu):
    def __init__(self, id):
        """ Tournament show menu """
        super().__init__(title=f"Tournament {id} Menu", choices=[
            ("Tournaments players sorted by name", f"/tournaments/{id}/info/players/name"),
            ("Tournaments players sorted by rank", f"/tournaments/{id}/info/players/rank"),
            ("List of all turns", f"/tournaments/{id}/info/turns"),
            ("List of all matches", f"/tournaments/{id}/info/matches"),
            ("Play tournament", f"/tournaments/{id}/play"),
            ("Previous menu", "/tournaments"),
        ])


class PickWinnerMenu(Menu):
    def __init__(self, player1_name: str, player2_name: str):
        """ Select a winner menu """
        super().__init__(title="Select the winner", choices=[
            (f"{player1_name} has won", 1.0),
            (player2_name + " has won", 0.0),
            ("It's a draw", 0.5),
        ])
