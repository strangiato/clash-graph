import royalerequest
import createnodes

def updateCards(graph, base_url, headers):
    cards = royalerequest.getCards(base_url, headers)

    for card in cards:
        createnodes.createCard(
            graph,
            card["key"],
            card["name"],
            card["elixir"],
            card["type"],
            card["rarity"],
            card["description"]
        )

def updateClan(graph, base_url, headers, tag):
    clan = royalerequest.getClan(base_url, headers, tag)

    clan_node = createnodes.createClan(
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
        createnodes.createPlayer(
            graph,
            player["tag"],
            player["name"],
            player["trophies"],
            player["role"],
            clan_node
        )

        clanMembers.append(player["tag"])

    return clanMembers

def updateBattles(graph, base_url, headers, tag):
    battles = royalerequest.getBattles(base_url, headers, tag)

    for battle in battles:
        # skip DoubleDeck_Tournaments because they use two decks for each player
        if battle["mode"]["name"] == "DoubleDeck_Tournament":
            continue

        team_node = updateTeam(graph, battle["team"])
        opponent_node = updateTeam(graph, battle["opponent"])

        createnodes.createBattle(
            graph,
            battle["type"],
            battle["utcTime"],
            battle["isLadderTournament"],
            battle["mode"]["name"],
            team_node,
            opponent_node
        )

def updateTeam(graph, team):
        team_list = []
        deck_list = []

        for player in team:
            
            clan_node = None
            # get the clan if they have one
            if player["clan"] is not None:
                clan_node = createnodes.createClan(
                    graph,
                    player["clan"]["tag"],
                    player["clan"]["name"]
                )

            team_list.append(createnodes.createPlayer(
                graph, 
                player["tag"],
                player["name"],
                clan_node=clan_node
            ))

            deck_list.append(createnodes.createDeck(
                graph,
                player["deck"]
            ))

        team_node = createnodes.createTeam(
            graph, 
            team_list, 
            deck_list
        )

        return team_node

if __name__ == "__main__":
    graph = createnodes.getGraph()
    base_url = royalerequest.getBaseURL()
    headers = royalerequest.getHeaders()

    clans = ["VV80RJY"]
    players = []

    updateCards(graph, base_url, headers)
    clan_members = updateClan(graph, base_url, headers, "VV80RJY")
    players.extend(clan_members)

    for player in players:
        updateBattles(graph, base_url, headers, player)