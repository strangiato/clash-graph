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
        player_node = createnodes.createPlayer(
            graph,
            player["tag"],
            player["name"],
            player["trophies"],
            player["role"],
            clan_node
        )

        clanMembers.append(player_node)

    return clanMembers

# def updateClan_old(tag):
#     clan = royalerequest.getClan(base_url, headers, tag)

#     node_clan = Clan()
#     node_clan.tag = clan["tag"]
#     node_clan.name = clan["name"]
#     node_clan.description = clan["description"]
#     node_clan.clan_type = clan["type"]
#     node_clan.score = clan["score"]
#     node_clan.warTrophies = clan["warTrophies"]
#     node_clan.memberCount = clan["memberCount"]
#     node_clan.requiredScore = clan["requiredScore"]
#     node_clan.donations = clan["donations"]

#     clash.push(node_clan)

#     for player in clan["members"]:
#         updatePlayer(player["tag"], node_clan)
#         updateBattles(player["tag"])

# def updatePlayer_old(tag, clan = None):
#     player = royalerequest.getPlayer(base_url, headers, tag)

#     node_player = Player()
#     node_player.tag = player["tag"]
#     node_player.name = player["name"]
#     if "role" in player["clan"]:
#         node_player.clan_role = player["clan"]["role"]
#     node_player.trophies = player["trophies"]
#     # node_player.donations = player["clan"]["donations"]
#     # node_player.donationsReceived = player["clan"]["donationsReceived"]
#     # node_player.donationsDelta = player["clan"]["donationsDelta"]

#     if clan != None:
#         node_player.member_of.add(clan)

#     clash.push(node_player)

#     return node_player

#     #updateDeck(player["currentDeck"], node_player)

# def updateDeck_old(deck, player):

#     """
#     Create a deck object with a unique hash of the cards

#     Keyword arguments:
#     deck -- a list of card json objects
#     player -- a GraphObject Player instance
#     """

#     assert(isinstance(player, Player))

#     node_deck = Deck()

#     deckKeys = []
#     deckElixier = []
    
#     for card in deck:
#         deckKeys.append(card["key"])
#         deckElixier.append(card["elixir"])

#         node_card = Card.match(clash, card["key"]).first()
#         node_deck.contains.add(node_card)

#     node_deck.setHash(deckKeys)
#     node_deck.calculateExilir(deckElixier)

#     node_deck.played.add(player)

#     clash.push(node_deck)

#     return node_deck

# def updateBattles_old(tag):
#     battles = royalerequest.getBattles(base_url, headers, tag)

#     for battle in battles:
#         node_battle = Battle()

#         node_battle.utcTime = battle["utcTime"]
#         node_battle.battle_type = battle["type"]
#         node_battle.isLadderTournament = battle["isLadderTournament"]
#         node_battle.battle_mode = battle["mode"]["name"]

#         node_battleTeam = updateBattleTeam(battle["team"])
#         node_battle.battled_in.add(node_battleTeam)

#         node_battleOpponent = updateBattleTeam(battle["opponent"])
#         node_battle.battled_in.add(node_battleOpponent)

#         clash.push(node_battle)

# def updateBattleTeam_old(team):
#     node_battleTeam = BattleTeam()
    
#     for player in team:
#         node_player = Player.match(clash, player["tag"]).first()

#         if not node_player:
#             node_player = updatePlayer(player["tag"])

#         node_battleTeam.played_in.add(node_player)

#         node_deck = updateDeck(player["deck"], node_player)

#         node_battleTeam.used_deck.add(node_deck)

#         clash.push(node_battleTeam)

#     return node_battleTeam

if __name__ == "__main__":
    graph = createnodes.getGraph()
    base_url = royalerequest.getBaseURL()
    headers = royalerequest.getHeaders()

    updateCards(graph, base_url, headers)
    updateClan(graph, base_url, headers, "VV80RJY")
