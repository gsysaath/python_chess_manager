from pydantic import ValidationError

from orm.player_orm import players
from orm.tournament_orm import tournaments
from controllers.router import Router

from views.menu_view import HomeMenu, PlayerMenu, TournamentMenu, TournamentShowMenu, SelectItemMenu
from views.form_view import NewPlayerForm, NewTournamentForm
from views.table_view import PlayerListByName, PlayerListByRank, TournamentList, TournamentPlayerListByName
from views.table_view import TournamentPlayerListByScore, TournamentTurns, TournamentMatches
from views.show_error import ShowError


router = Router()


def main():
    """ Main Menu """
    router.navigate(HomeMenu().exec())


def create_player():
    """ Create player """
    form_data = NewPlayerForm().exec()
    try:
        players.create(save=True, **form_data)
    except (ValidationError, ValueError) as e:
        ShowError(str(e)).exec()
    router.navigate('/players')


def create_tournament():
    """ Create tournament """
    form_data = NewTournamentForm().exec()
    try:
        tournaments.create(save=True, **form_data)
    except (ValidationError, ValueError) as e:
        ShowError(str(e)).exec()
    router.navigate("/tournaments")


def players_menu():
    """ Show players menu """
    router.navigate(PlayerMenu().exec())


def players_list_by_name():
    """ Show players list sorted by name """
    PlayerListByName().exec()
    router.navigate("/players")


def players_list_by_rank():
    """ Show players list sorted by rank """
    PlayerListByRank().exec()
    router.navigate("/players")


def tournaments_menu():
    """ Show tournament menu """
    router.navigate(TournamentMenu().exec())


def tournaments_all():
    """ Show all tournaments list """
    TournamentList().exec()
    router.navigate("/tournaments")


def show_tournament(tournament_id=None):
    """ Show one tournament details menu """
    if tournament_id is None:
        tournament_id = SelectItemMenu(items=tournaments.find_all()).exec()
    name = tournaments.find_by_id(tournament_id).name
    router.navigate(TournamentShowMenu(id=tournament_id, tournament_name=name).exec(), has_param=True)


def tournaments_players_name(id):
    """ Show one tournament players list sorted by name """
    players_ids = tournaments.find_by_id(id).players
    players_list = []
    for player_id in players_ids:
        players_list.append(players.find_by_id(player_id))
    players_list = sorted(players_list, key=lambda x: (x.last_name, x.first_name))
    TournamentPlayerListByName(players_list).exec()
    show_tournament(tournament_id=id)


def tournaments_players_score(id):
    """ Show one tournament players list sorted by score """
    tournament = tournaments.find_by_id(id)
    players_ids = tournaments.find_by_id(id).players
    players_list = []
    for player_id in players_ids:
        players_list.append(players.find_by_id(player_id))
    if tournament.turns[0].matches[0].player1_score is not None:
        players_list = sorted(players_list, key=lambda player: (-tournament.get_player_score(player.id), -player.rank))
        players_list_and_score = []
        for player in players_list:
            players_list_and_score.append(f"{player.name} - Score: {tournament.get_player_score(player.id)}")
        TournamentPlayerListByScore(players_list_and_score).exec()
    else:
        TournamentPlayerListByScore(["No match played yet."]).exec()
    router.navigate(f"/tournaments/{id}/info", has_param=True)


def tournaments_turns(id):
    """ Show one tournament turns """
    turns_list = tournaments.find_by_id(id).turns
    TournamentTurns(turns_list).exec()
    router.navigate(f"/tournaments/{id}/info", has_param=True)


def tournaments_matches(id):
    """ Show one tournament matches """
    turns_list = tournaments.find_by_id(id).turns
    matches_list = []
    for turn in turns_list:
        for match in turn.matches:
            matches_list.append(match)
    TournamentMatches(matches_list).exec()
    router.navigate(f"/tournaments/{id}/info", has_param=True)


def tournament_play(id):
    """ Play the tournament """
    tournaments.find_by_id(id).play(tournaments)
    router.navigate(f"/tournaments/{id}/info", has_param=True)
