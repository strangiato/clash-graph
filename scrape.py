from py2neo import Graph

from graphmodels import Clan, Player, Card, Deck, Battle, BattleTeam
import royalerequest

clash = Graph(host = "localhost", auth=("neo4j", "test123"))

def updateCards():
    cards = royalerequest.getCards(base_url, headers)

    for card in cards:
        node_card = Card()
        node_card.key = card["key"]
        node_card.name = card["name"]
        node_card.elixir = card["elixir"]
        node_card.card_type = card["type"]
        node_card.rarity = card["rarity"]
        node_card.description = card["description"]
        clash.push(node_card)

def updateClan(tag):
    clan = royalerequest.getClan(base_url, headers, tag)

    node_clan = Clan()
    node_clan.tag = clan["tag"]
    node_clan.name = clan["name"]
    node_clan.description = clan["description"]
    node_clan.clan_type = clan["type"]
    node_clan.score = clan["score"]
    node_clan.warTrophies = clan["warTrophies"]
    node_clan.memberCount = clan["memberCount"]
    node_clan.requiredScore = clan["requiredScore"]
    node_clan.donations = clan["donations"]

    clash.push(node_clan)

    for player in clan["members"]:
        updatePlayer(player["tag"], node_clan)
        updateBattles(player["tag"])

def updatePlayer(tag, clan = None):
    player = royalerequest.getPlayer(base_url, headers, tag)

    node_player = Player()
    node_player.tag = player["tag"]
    node_player.name = player["name"]
    if "role" in player["clan"]:
        node_player.clan_role = player["clan"]["role"]
    node_player.trophies = player["trophies"]
    # node_player.donations = player["clan"]["donations"]
    # node_player.donationsReceived = player["clan"]["donationsReceived"]
    # node_player.donationsDelta = player["clan"]["donationsDelta"]

    if clan != None:
        node_player.member_of.add(clan)

    clash.push(node_player)

    return node_player

    #updateDeck(player["currentDeck"], node_player)

def updateDeck(deck, player):

    """
    Create a deck object with a unique hash of the cards

    Keyword arguments:
    deck -- a list of card json objects
    player -- a GraphObject Player instance
    """

    assert(isinstance(player, Player))

    node_deck = Deck()

    deckKeys = []
    deckElixier = []
    
    for card in deck:
        deckKeys.append(card["key"])
        deckElixier.append(card["elixir"])

        node_card = Card.match(clash, card["key"]).first()
        node_deck.contains.add(node_card)

    node_deck.setHash(deckKeys)
    node_deck.calculateExilir(deckElixier)

    node_deck.played.add(player)

    clash.push(node_deck)

    return node_deck

def updateBattles(tag):
    battles = royalerequest.getBattles(base_url, headers, tag)

    for battle in battles:
        node_battle = Battle()

        node_battle.utcTime = battle["utcTime"]
        node_battle.battle_type = battle["type"]
        node_battle.isLadderTournament = battle["isLadderTournament"]
        node_battle.battle_mode = battle["mode"]["name"]

        node_battleTeam = updateBattleTeam(battle["team"])
        node_battle.battled_in.add(node_battleTeam)

        node_battleOpponent = updateBattleTeam(battle["opponent"])
        node_battle.battled_in.add(node_battleOpponent)

        clash.push(node_battle)

def updateBattleTeam(team):
    node_battleTeam = BattleTeam()
    
    for player in team:
        node_player = Player.match(clash, player["tag"]).first()

        if not node_player:
            node_player = updatePlayer(player["tag"])

        node_battleTeam.played_in.add(node_player)

        node_deck = updateDeck(player["deck"], node_player)

        node_battleTeam.used_deck.add(node_deck)

        clash.push(node_battleTeam)

    return node_battleTeam

if __name__ == "__main__":
    base_url = royalerequest.getBaseURL()
    headers = royalerequest.getHeaders()

    updateCards()
    updateClan("VV80RJY")
