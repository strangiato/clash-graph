import royalerequest
import createnodes


def update_cards(graph, base_url, headers):
    cards = royalerequest.get_cards(base_url, headers)

    for card in cards:
        createnodes.create_card(
            graph,
            card["key"],
            card["name"],
            card["elixir"],
            card["type"],
            card["rarity"],
            card["description"]
        )


def update_clan(graph, base_url, headers, tag):
    clan = royalerequest.get_clan(base_url, headers, tag)

    clan_node = createnodes.create_clan(
        graph,
        clan["tag"],
        clan["name"],
        clan["description"],
        clan["type"],
        clan["score"],
        clan["warTrophies"],
        clan["requiredScore"],
        clan["donations"]
    )

    clanMembers = []

    for player in clan["members"]:
        createnodes.create_player(
            graph,
            player["tag"],
            player["name"],
            player["trophies"],
            player["role"],
            clan_node
        )

        clanMembers.append(player["tag"])

    return clanMembers


def update_battles(graph, base_url, headers, tag):
    battles = royalerequest.get_battles(base_url, headers, tag)

    MODES = [
        "Touchdown_MegaDeck_Challenge",
        "Touchdown_MegaDeck_Ladder",
        "DoubleDeck_Tournament",
        "DoubleDeck_Friendly"
    ]

    for battle in battles:
        # skip game modes because they use two decks for each player
        if battle["mode"]["name"] in MODES:
            continue

        team_node = update_team(graph, battle["team"])
        opponent_node = update_team(graph, battle["opponent"])

        createnodes.create_battle(
            graph,
            battle["type"],
            battle["utcTime"],
            battle["isLadderTournament"],
            battle["mode"]["name"],
            team_node,
            opponent_node
        )


def update_team(graph, team):
        team_list = []
        deck_list = []

        for player in team:
            
            clan_node = None
            # get the clan if they have one
            if player["clan"] is not None:
                clan_node = createnodes.create_clan(
                    graph,
                    player["clan"]["tag"],
                    player["clan"]["name"]
                )

            team_list.append(createnodes.create_player(
                graph, 
                player["tag"],
                player["name"],
                clan_node=clan_node
            ))

            deck_list.append(createnodes.create_deck(
                graph,
                player["deck"]
            ))

        team_node = createnodes.create_team(
            graph, 
            team_list, 
            deck_list
        )

        return team_node


if __name__ == "__main__":
    graph = createnodes.get_graph()
    BASE_URL = royalerequest.get_base_url()
    HEADERS = royalerequest.get_headers()

    clans = ["VV80RJY"]
    players = []

    update_cards(graph, BASE_URL, HEADERS)

    for clan in clans:
        clan_members = update_clan(graph, BASE_URL, HEADERS, clan)
        players.extend(clan_members)

    for player in players:
        update_battles(graph, BASE_URL, HEADERS, player)
