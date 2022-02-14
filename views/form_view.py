from enum import EnumMeta
from datetime import date
from typing import Any, Dict, List, Optional, Tuple

from orm.player_orm import players

from models.player import Gender
from models.tournament import TimeControl
from models.custom_types import (
    Name,
    Rank,
    TimeControlInt,
)

from views.view import View
from views.menu_view import EnumMenu, SelectItemMenu


class Form(View):
    """
    """
    def __init__(self, title: str, fields: List[Tuple[str, str, Any, Optional[Any]]]):
        super().__init__(title)
        self.fields = fields
        self.template = "\n".join(f"{field[1].title()} : {{{field[0]}}}" for field in fields)

    def render_template(self, **params):
        """ Renders template """
        self.content = self.template.format(
            **{k: (v if v is not None else "N/A") for k, v in params.items()}
        )

    def post_exec(self, data: Dict[str, Any]):
        """ Treat fields input """
        return data

    def gen_empty_data(self):
        """ Generate empty dictionnary from initial value """
        data = {}
        for field in self.fields:
            match field:
                case name, _, _:
                    pass
                case name, _, _, _:
                    pass
            data[name] = None
        return data

    def exec(self):
        """ Execute the view to allow user to input data """
        data = self.gen_empty_data()
        for field in self.fields:
            match field:
                case name, description, field_type:
                    default_value = None
                case name, description, field_type, default_value:
                    pass
            while True:
                self.render_template(**data)
                super().exec()
                try:
                    if isinstance(field_type, EnumMeta):
                        try:
                            data[name] = EnumMenu(title="", enum=field_type).exec(clear=False)
                            break
                        except ValueError:
                            continue
                except TypeError:
                    pass
                try:
                    raw = input(description.title() + " ? ")
                    if not raw and default_value is not None:
                        raw = default_value
                    data[name] = field_type(raw)
                    break
                except ValueError:
                    pass
        self.render_template(**data)
        self.blocking = True
        super().exec()
        return self.post_exec(data)


class NewPlayerForm(Form):
    def __init__(self):
        """ Initialize new player form """
        super().__init__(title="New Player Form", fields=[
            ('last_name', 'last name', Name),
            ('first_name', 'first name', Name),
            ('birth_date_day', 'birthdate day', int),
            ('birth_date_month', 'birthdate month', int),
            ('birth_date_year', 'birthdate year', int),
            ('gender', 'gender (M or F)', Gender),
            ('rank', 'rank (between 1 and 3000)', Rank),
        ])

    def post_exec(self, data):
        data['birth_date'] = date(year=data['birth_date_year'],
                                  month=data['birth_date_month'], day=data['birth_date_day'])
        return data


class NewTournamentForm(Form):
    def __init__(self):
        """ Initialize new tournament form """
        super().__init__(title="New Tournament Form", fields=[
            ('name', "tournament name", str),
            ('place', "tournament place", str),
            ('start_day', 'start date day', int, date.today().day),
            ('start_month', 'start date month', int, date.today().month),
            ('start_year', 'start date year', int, date.today().year),
            ('number_of_turns', 'number of turns', int, 4),
            ('time_control', 'Time Control (1: Bullet, 2: Blitz, 3: Rapid)', TimeControlInt, 3),
            ('description', 'description', str),
            ('number_of_players', 'number of players', int),
        ])

    def post_exec(self, data):
        data['time_control'] = TimeControl(data['time_control'])
        select_player_menu = SelectItemMenu(players.find_all())
        data['players'] = [select_player_menu.exec() for _ in range(data['number_of_players'])]
        data["turns"] = [{'name': f"round {nb}", 'position': nb} for nb in range(1, data['number_of_turns'] + 1)]
        return data
