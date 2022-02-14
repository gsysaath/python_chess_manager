from orm.player_orm import players
from orm.tournament_orm import tournaments
# from tournament_orm import tournaments

from views.view import View


class Table(View):
    def __init__(self, title: str, item_list: list):
        """ Show list of items """
        content = '\n'.join(
            [f'{item}' for item in item_list])
        super().__init__(title=title, content=content, blocking=True)


class PlayerListByName(Table):
    def __init__(self):
        """ Show players list sorted by name """
        player_list = players.find(sort_key=lambda x: (
            x.last_name, x.first_name, -x.rank))
        super().__init__(title="Players list sorted by name", item_list=player_list)


class PlayerListByRank(Table):
    def __init__(self):
        """ Show players rank sorted by rank """
        player_list = players.find(
            sort_key=lambda x: (-x.rank, x.last_name, x.first_name))
        super().__init__(title="Players list sorted by rank", item_list=player_list)


class TournamentList(Table):
    def __init__(self):
        """ Show tournaments list """
        tournament_list = tournaments.find_all()
        super().__init__(title="List of all tournaments", item_list=tournament_list)


class TournamentTurns(Table):
    def __init__(self, turns_list):
        """ Show tournament's turns """
        super().__init__(title="Turns", item_list=turns_list)


class TournamentMatches(Table):
    def __init__(self, matches_list):
        """ Show tournament's matches """
        super().__init__(title="Turns", item_list=matches_list)


class TournamentPlayerListByName(Table):
    def __init__(self, players_list):
        """ Show tournament's players sorted by name """
        super().__init__(title="Players list sorted by Name in this tournament", item_list=players_list)


class TournamentPlayerListByScore(Table):
    def __init__(self, players_list):
        """ Show tournament's players sorted by score """
        super().__init__(title="Players list sorted by Score in this tournament", item_list=players_list)
