from controllers.controllers import (
    router,
    main,
    create_player,
    create_tournament,
    players_menu,
    players_list_by_name,
    players_list_by_rank,
    tournaments_menu,
    tournaments_all,
    show_tournament,
    tournaments_players_name,
    tournaments_players_score,
    tournaments_turns,
    tournaments_matches,
    tournament_play,
)

router.add_route("/", main)
router.add_route("/players", players_menu)
router.add_route("/players/add", create_player)
router.add_route("/tournaments", tournaments_menu)
router.add_route("/players/all/sort-by-name", players_list_by_name)
router.add_route("/players/all/sort-by-rank", players_list_by_rank)
router.add_route("/tournaments/all", tournaments_all)
router.add_route("/tournaments/add", create_tournament)
router.add_route("/tournaments/info", show_tournament)
router.add_route("/tournaments/info/players/name", tournaments_players_name)
router.add_route("/tournaments/info/players/rank", tournaments_players_score)
router.add_route("/tournaments/info/turns", tournaments_turns)
router.add_route("/tournaments/info/matches", tournaments_matches)
router.add_route("/tournaments/play", tournament_play)

if __name__ == '__main__':
    main()

# Custom types/ turn start datetime setting, try except when create, form_view change class to custom types
# Docstring to all functions/ AND READ ME +  Powerpoint + github
# Wording turns => matches
# Wording rank => score
# flake8_html => reporting
